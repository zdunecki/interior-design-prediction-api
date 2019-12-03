import boto3
from datetime import datetime
import os

REGION = os.getenv("SPACE_REGION", "")
URL = os.getenv("SPACE_URL", "")
ACCESS_KEY_ID = os.getenv("SPACE_ACCESS_KEY_ID", "")
ACCESS_SECRET_KEY = os.getenv("SPACE_ACCESS_SECRET_KEY", "")
BUCKET_NAME = os.getenv("SPACE_BUCKET_NAME", "")
FILE_NAME = "dump.tar.gz"

data = open(FILE_NAME, 'rb')

s3 = boto3.resource(
    's3',
    region_name=REGION,
    endpoint_url=URL,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY
)
bucket = s3.Bucket(BUCKET_NAME)

output_path = "mongo/dumps/" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "/" + FILE_NAME
bucket.put_object(Key=output_path, Body=data)
print("Done")
