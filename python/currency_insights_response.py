import json
import decimal

class CurrencyInsightsResponse:

    def __init__(self, data):
        self.data = data

    def format_body(self):
        return json.dumps(self.replace_decimals(self.data))

    def format_ok(self):
        result = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE,PATCH',
                'Access-Control-Allow-Origin': '*'
            },
            'body': self.format_body()
        }
        return result

    def replace_decimals(self, obj):
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = self.replace_decimals(obj[i])
            return obj
        elif isinstance(obj, dict):
            for k in obj:
                obj[k] = self.replace_decimals(obj[k])
            return obj
        elif isinstance(obj, decimal.Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        else:
            return obj