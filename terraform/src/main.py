import boto3
import json
import os
import traceback
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_environment_variable(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is not set.")
    return value

def list_objects_in_bucket(s3, bucket_name):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            yield from page['Contents']
        else:
            print(f"No objects found in {bucket_name}.")

def copy_object(s3, source_bucket, destination_bucket, source_key):
    copy_source = {'Bucket': source_bucket, 'Key': source_key}
    dest_key = source_key
    try:
        s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=dest_key)
        print(f'Successfully copied {source_bucket}/{source_key} to {destination_bucket}/{dest_key}')
        return dest_key
    except Exception as e:
        print(f'Error copying object {source_key}: {e}')
        traceback.print_exc()
        return None

def count_objects_in_bucket(s3, bucket_name):
    count = 0
    for _ in list_objects_in_bucket(s3, bucket_name):
        count += 1
    return count

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        source_bucket = get_environment_variable('SOURCE_BUCKET')
        destination_bucket = get_environment_variable('DESTINATION_BUCKET')

        copied_objects = []

        # Copy objects from source to destination
        for obj in list_objects_in_bucket(s3, source_bucket):
            dest_key = copy_object(s3, source_bucket, destination_bucket, obj['Key'])
            if dest_key:
                copied_objects.append(dest_key)

        if not copied_objects:
            message = "No objects copied from source to destination buckets."
            print(message)
            raise Exception(message)

        # Count objects in both source and destination buckets
        source_count = count_objects_in_bucket(s3, source_bucket)
        destination_count = count_objects_in_bucket(s3, destination_bucket)

        if source_count != destination_count:
            message = (f"Object count mismatch: Source bucket ({source_bucket}) has {source_count} objects, "
                       f"but destination bucket ({destination_bucket}) has {destination_count} objects.")
            print(message)
            raise Exception(message)

        message = f"Challenge complete - S3 objects copied successfully: {', '.join(copied_objects)}"
        print(message)
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
    except (ValueError, NoCredentialsError, PartialCredentialsError) as e:
        print(f'Configuration error: {e}')
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps(f'Configuration error: {e}')
        }
    except Exception as e:
        print(f'Error: {e}')
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e}')
        }

if __name__ == '__main__':
    lambda_handler(None, None)
