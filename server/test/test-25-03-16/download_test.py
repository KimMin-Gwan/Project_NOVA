import boto3
import cv2
path = './model/local_database/'
service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
sregion_name = 'kr-standard'
access_key = 'eeJ2HV8gE5XTjmrBCi48'
secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
s3 = boto3.client(service_name,
                    endpoint_url=endpoint_url,
                   aws_access_key_id=access_key,
              aws_secret_access_key=secret_key)

s3.download_file('nova-images','1001.PNG','./cv2_test/1001.png')
       