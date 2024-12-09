from aws_service_provider import AwsServiceProvider
from data_service import DataService


class ServiceLookup:

    def __init__(self):
        self.aws_service_provider = AwsServiceProvider()
        self.data_service = DataService(self.aws_service_provider.get_dynamodb())
