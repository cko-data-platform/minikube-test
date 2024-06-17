import boto3
import json
import os
import traceback

def lambda_handler(event, context):
    # Get the S3 client
    s3 = boto3.client('s3')

    # Get environment variables
    source_bucket = os.getenv('SOURCE_BUCKET')
    destination_bucket = os.getenv('DESTINATION_BUCKET')

    # List objects in the source bucket
    try:
        response = s3.list_objects_v2(Bucket=source_bucket)
        print(response)
        
        if 'Contents' not in response:
            print('No objects found in the source bucket.')
            return {
                'statusCode': 200,
                'body': json.dumps('No objects to process')
            }
        
        copied_objects = []

        for obj in response['Contents']:
            source_key = obj['Key']
            
            # Copy the object to the destination bucket
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            dest_key = source_key.replace('source/', 'destination/')
            
            try:
                s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=dest_key)
                print(f'Successfully copied {source_key} to {dest_key}')
                copied_objects.append(dest_key)
            except Exception as e:
                print(f'Error copying object: {e}')
                traceback.print_exc()
                # Log the specific error for debugging purposes
                continue
        
        # Check if any objects were successfully copied
        if copied_objects is None:
            raise Exception("No objects copied from source to destination buckets.")
        
        # Construct response message
        message = f"Challenge complete - S3 objects copied successfully: {', '.join(copied_objects)}"
        print(message)
        
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
        
    except Exception as e:
        print(f'Error: {e}')
        traceback.print_exc()
        raise e

# If running this script locally, invoke lambda_handler directly without an event
if __name__ == '__main__':
    lambda_handler(None, None)
