import decimal
from boto3.dynamodb.conditions import Key

TABLE_NAME = 'CurrencyInsights-CurrencyData'


class DataService:

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
        self.currency_data_table = dynamodb.Table(TABLE_NAME)

    def create_currency_data(self, currency_code: str, date: str, rate: float, previous_day_rate: float, rate_change: float):
        existing = self.currency_data_table.get_item(Key={'currency_code': currency_code, 'date': date})
        if existing.get('Item'):
            pass
        else:
            self.currency_data_table.put_item(Item={
                'currency_code': currency_code,
                'date': date,
                'rate': decimal.Decimal(rate),
                'previous_day_rate': decimal.Decimal(previous_day_rate),
                'rate_change': decimal.Decimal(rate_change)
            })

    def get_currency_data_by_date(self, date: str):
        response = self.currency_data_table.query(
            IndexName='DateIndex',
            KeyConditionExpression=Key('date').eq(date)
        )
        result = response['Items'] if response.get('Items') is not None else []
        return result

    def get_currency_data(self, currency_code: str, date: str):
        response = self.currency_data_table.get_item(Key={'currency_code': currency_code, 'date': date})
        return response['Item'] if response.get('Item') else None
