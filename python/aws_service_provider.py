import boto3

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')


class AwsServiceProvider:

    def __init__(self):
        pass

    def get_dynamodb(self):
        return dynamodb

    def get_s3_client(self):
        return s3_client
