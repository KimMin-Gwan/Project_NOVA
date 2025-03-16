import boto3

service_name = "s3"
endpoint = "https://kr.object.ncloudstorage.com"
secret_key='zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
access_key='eeJ2HV8gE5XTjmrBCi48'

s3 = boto3.client(
            service_name,
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

bucket_name = 'removetest'
for i in s3.list_objects(Bucket=bucket_name, MaxKeys=255)['Contents']:
    s3.delete_object(Bucket=bucket_name, Key=i['Key'])
