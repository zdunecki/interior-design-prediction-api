import boto3
from botocore.client import Config

# Initialize a session using DigitalOcean Spaces.
client = boto3.client('s3',
                      endpoint_url='http://fra1.digitaloceanspaces.com',
                      aws_access_key_id='CLHSHSLW3ZQZ7SXSFC7Q',
                      aws_secret_access_key='SPACE_SECRET_ACCESS_KEY')

response = client.list_buckets()
# spaces = [space['Name'] for space in response['Buckets']]
# print("Spaces List: %s" % spaces)

print(client)
