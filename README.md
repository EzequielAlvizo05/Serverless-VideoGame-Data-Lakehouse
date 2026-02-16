# Serverless Video Game Data Lakehouse: Automated ETL Pipeline

This project implements an end-to-end automated Data Lakehouse architecture on AWS to analyze video game market trends using the RAWG API. Developed by Jose Ezequiel Alvizo De La Cruz, 9th-semester Data and Organizational Intelligence Engineering student.

## Architecture and Workflow

The system follows an event-driven, serverless approach using a Medallion Architecture (Bronze and Gold layers).

1. Ingestion (Bronze Layer):
   An Amazon EventBridge rule triggers an AWS Lambda function every Sunday at 00:00 UTC. This function fetches data from the RAWG API and stores the raw JSON in an S3 Bronze bucket.

2. Automated Transformation (Gold Layer):
   An S3 Object Created event triggers a second AWS Lambda function. Using Pandas and AWS SDK for Pandas (Wrangler), the data is:
   - Flattened and cleaned.
   - Partitioned by Year and Month (Hive-style) for query optimization.
   - Converted to Apache Parquet format.
   - Saved into the S3 Gold bucket.

3. Schema Evolution and Cataloging:
   The transformation Lambda utilizes AWS Wrangler to automatically update the AWS Glue Data Catalog. This "Crawler-less" approach ensures real-time schema synchronization and cost efficiency by avoiding periodic Glue Crawler runs.

4. Data Lifecycle Management:
   S3 Lifecycle Policies are implemented to manage storage costs:
   - Bronze Layer: Raw JSON files expire after 7 days.
   - Technical Cleanup: Incomplete multipart uploads are deleted after 1 day.

5. Analytics and Consumption:
   - Amazon Athena: Serves as the serverless SQL engine to query the partitioned Parquet files.
   - Streamlit Cloud: Provides a professional business intelligence dashboard, connected via PyAthena and secured with Streamlit Secrets.

## Tech Stack

- Cloud: AWS (Lambda, S3, EventBridge, Glue, Athena, IAM)
- Language: Python 3.12
- Libraries: pandas, awswrangler, boto3, pyathena, streamlit
- Data Formats: JSON, Parquet (Columnar Storage)

## Engineering Best Practices

- FinOps: Implementation of AWS Budgets with threshold alerts to prevent unexpected cloud costs.
- Performance: Hive-style partitioning (year/month) to reduce data scanning in Athena.
- Security: Principle of Least Privilege (PoLP) applied via IAM Roles and resource-based policies for EventBridge.
- Automation: Fully event-driven pipeline with zero manual intervention required for weekly updates.

## Setup and Installation

1. Repository Setup:
   git clone https://github.com/EzequielAlvizo05/Serverless-VideoGame-Data-Lakehouse.git

2. Dependency Management:
   Install required libraries using: pip install -r requirements.txt

3. Environment Configuration:
   Create a .streamlit/secrets.toml file (ignored by git) with the following keys:
   AWS_ACCESS_KEY_ID = "your_access_key"
   AWS_SECRET_ACCESS_KEY = "your_secret_key"
   AWS_REGION = "us-east-1"

4. Execution:
   Run the local dashboard: streamlit run Proyecto1/app.py

## Business Insights (Organizational Intelligence)

Aligned with the Organizational Intelligence focus, this project provides:

- Market Trend Analysis: Identification of high-performing genres and platforms.
- Player Engagement Metrics: Correlation between playtime, ratings, and critic scores.
- Strategic Resource Allocation: Data-driven insights for investment in specific game categories.
