# SD-project
SystemDesign_Project

## Project Description
Build a distributed system for an ETL pipeline. We're extracting data on nurses from multiple hospitals, and presenting our findings via visualizations

## Constraints

Each row of data is 1kb in size. Our network can only handle 1mb in throughput. There we will run batch jobs 1MB in size (1000) rows long and send them through the network


## Architecture

## Extract
Move data from CSV files in batches (1000 rows per batch)

## Transform
Alter data to fit the use case

## Load
Load data into the data warehouse

## Data Queue
Redis queues will take data from each pipeline portion once their respective process is complete.

