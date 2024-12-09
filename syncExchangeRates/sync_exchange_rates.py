from currency_insights_response import CurrencyInsightsResponse
from datetime import datetime, timedelta
from service_lookup import ServiceLookup
import decimal

def lambda_handler(event, context):
    print(f'Event received: {event}')
    current_date = datetime.now().strftime("%Y-%m-%d")
    previous_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    service_lookup = ServiceLookup()
    return SyncExchangeRatesHandler(service_lookup.data_service).sync_exchange_rates(current_date, previous_date)


class SyncExchangeRatesHandler:

    def __init__(self, data_service):
        self.data_service = data_service

    def sync_exchange_rates(self, current_date, previous_date):
        rates, message = self._get_currency_data_from_exchange()
        if rates:
            for rate in rates:
                previous_data = self.data_service.get_currency_data(currency_code=rate['@currency'], date=previous_date)
                previous_rate = previous_data["rate"] if previous_data else 0
                print(f"Previous Rate: {previous_rate}")
                self.data_service.create_currency_data(
                    currency_code=rate['@currency'],
                    date=current_date,
                    rate=rate['@rate'],
                    previous_day_rate=previous_rate,
                    rate_change=abs(previous_rate-decimal.Decimal(rate['@rate'])),
                )
                new_data = self.data_service.get_currency_data(currency_code=rate['@currency'], date=current_date)
                print(f"New Data: {new_data}")

            response = {
                'Message': "Exchange Rates Synced Successfully"
            }
            return CurrencyInsightsResponse(response).format_ok()
        else:
            return CurrencyInsightsResponse(message).format_ok()

    @staticmethod
    def _get_currency_data_from_exchange():
        import requests
        import xmltodict
        try:
            url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
            response = requests.get(url)
            data = xmltodict.parse(response.content)
            rates = data['gesmes:Envelope']['Cube']['Cube']['Cube']
            return rates, {"Message": "Success"}
        except Exception as e:
            return None, {"Message": f"Error: {e}"}
