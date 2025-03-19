import os
import boto3
from google.oauth2 import service_account
from googleapiclient.discovery import build

# AWS S3 Configuration
# S3_BUCKET = "your-s3-bucket-name" 
S3_BUCKET = "myhealthcarebucket-01"

# Path to Google Drive Service Account JSON file
# SERVICE_ACCOUNT_FILE = "service_account.json" 
SERVICE_ACCOUNT_FILE = "extract/healthcare-etl-451423-157219db4103.json"

# Google Drive Folder ID where CSV files are stored
# GOOGLE_DRIVE_FOLDER_ID = "your-google-drive-folder-id"
GOOGLE_DRIVE_FOLDER_ID = "1LmIYUeTIrWNEc1Au7imkJEYqFqfRPXLy" 

# Initialize AWS S3 client
s3_client = boto3.client("s3")

def authenticate_drive():
    """Authenticate using the service account JSON file."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def list_csv_files(drive_service):
    """List all CSV files in the specified Google Drive folder."""
    query = f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and mimeType='text/csv'"
    results = drive_service.files().list(q=query).execute()
    return results.get("files", [])
    
    # if not files:
    #     print("No CSV files found.")
    #     return
    
<<<<<<< HEAD
    # print("\n📂 Found CSV Files in Google Drive:")
=======
    # print("\n Found CSV Files in Google Drive:")
>>>>>>> origin/main
    # for file in files:
    #     print(f"- {file['name']} (ID: {file['id']})")

def download_file(drive_service, file_id, file_name):
    # """Download file from Google Drive."""
    # request = drive_service.files().get_media(fileId=file_id)
    # file_path = f"/tmp/{file_name}"  # Use /tmp directory for AWS Lambda compatibility
    # with open(file_path, "wb") as f:
    #     f.write(request.execute())
    # return file_path
    """Ensure /tmp/ exists before writing files."""
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)  # Create /tmp/ if it does not exist

    file_path = os.path.join(tmp_dir, file_name)
    request = drive_service.files().get_media(fileId=file_id)
    
    with open(file_path, "wb") as f:
        f.write(request.execute())  # Ensure file content is properly written

<<<<<<< HEAD
    print(f"✅ File downloaded: {file_path} ({os.path.getsize(file_path)} bytes)")
=======
    print(f"File downloaded: {file_path} ({os.path.getsize(file_path)} bytes)")
>>>>>>> origin/main
    return file_path


def upload_to_s3(file_path, file_name):
    """Upload file to S3 bucket."""
    s3_key = f"raw/{file_name}"  # Save in 'raw' folder inside S3
    s3_client.upload_file(file_path, S3_BUCKET, s3_key)
<<<<<<< HEAD
    print(f"✅ Uploaded {file_name} to s3://{S3_BUCKET}/{s3_key}")
=======
    print(f"Uploaded {file_name} to s3://{S3_BUCKET}/{s3_key}")
>>>>>>> origin/main

def process_files():
    """Main function to download and upload CSV files."""
    drive_service = authenticate_drive()
    files = list_csv_files(drive_service)

    if not files:
        print("No new CSV files found in Google Drive.")
        return

    for file in files:
        file_id = file['id']
        file_name = file['name']
<<<<<<< HEAD
        print(f"📥 Downloading: {file_name}")
=======
        print(f"Downloading: {file_name}")
>>>>>>> origin/main

        file_path = download_file(drive_service, file_id, file_name)
        upload_to_s3(file_path, file_name)
        os.remove(file_path)  # Cleanup temporary file

<<<<<<< HEAD
    print("🎉 All files processed successfully.")
=======
    print("All files processed successfully.")
>>>>>>> origin/main

if __name__ == "__main__":
    process_files()
