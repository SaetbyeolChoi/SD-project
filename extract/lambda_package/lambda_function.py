import os
import boto3
from google.oauth2 import service_account
from googleapiclient.discovery import build
from boto3.dynamodb.conditions import Key
import json

# AWS Configuration
S3_BUCKET = os.environ['S3_BUCKET'] 
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE'] 

# Google Drive Configuration
SERVICE_ACCOUNT_FILE = "/tmp/service_account.json"
GOOGLE_DRIVE_FOLDER_ID = os.environ['GOOGLE_DRIVE_FOLDER_ID']

# AWS Clients
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

def authenticate_drive():
    """Authenticate with Google Drive API."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def get_processed_files():
    """Retrieve processed file_ids from DynamoDB."""
    response = table.scan()
    return {item["file_id"]: item["modified_time"] for item in response.get("Items", [])}

def list_google_drive_files(drive_service):
    """List all CSV files in the Google Drive folder."""
    query = f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and mimeType='text/csv'"
    results = drive_service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    return results.get("files", [])

def download_file(drive_service, file_id, file_name):
    """Download file from Google Drive."""
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    file_path = os.path.join(tmp_dir, file_name)
    request = drive_service.files().get_media(fileId=file_id)
    
    with open(file_path, "wb") as f:
        f.write(request.execute())

    print(f"Downloaded {file_name} ({os.path.getsize(file_path)} bytes)")
    return file_path

def upload_to_s3(file_path, file_name):
    """Upload file to S3 bucket."""
    s3_key = f"raw/{file_name}"
    s3_client.upload_file(file_path, S3_BUCKET, s3_key)
    print(f"Uploaded {file_name} to s3://{S3_BUCKET}/{s3_key}")

def update_dynamodb(file_id, modified_time):
    """Update processed files in DynamoDB."""
    table.put_item(Item={"file_id": file_id, "modified_time": modified_time})

def lambda_handler(event, context):
    """Lambda function for incremental processing."""
    # Load Google Drive credentials from S3
    s3_client.download_file(S3_BUCKET, "service_account.json", "/tmp/service_account.json")

    drive_service = authenticate_drive()
    processed_files = get_processed_files()
    drive_files = list_google_drive_files(drive_service)

    new_files = [
        file for file in drive_files
        if file["id"] not in processed_files or file["modifiedTime"] > processed_files[file["id"]]
    ]

    if not new_files:
        print("No new files to process.")
        return {"statusCode": 200, "body": json.dumps("No new files found.")}

    for file in new_files:
        file_id, file_name, modified_time = file["id"], file["name"], file["modifiedTime"]
        print(f"Processing new file: {file_name}")

        file_path = download_file(drive_service, file_id, file_name)
        upload_to_s3(file_path, file_name)
        update_dynamodb(file_id, modified_time)
        os.remove(file_path)

    return {"statusCode": 200, "body": json.dumps("Files successfully processed.")}
