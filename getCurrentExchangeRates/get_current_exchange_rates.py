from currency_insights_response import CurrencyInsightsResponse
from datetime import datetime
from service_lookup import ServiceLookup


def lambda_handler(event, context):
    print(f'Event received: {event}')
    current_date = datetime.now().strftime("%Y-%m-%d")
    service_lookup = ServiceLookup()

    return GetCurrencyExchangeRatesHandler(service_lookup.data_service).get_currency_exchange_rates(current_date)


class GetCurrencyExchangeRatesHandler:

    def __init__(self, data_service):
        self.data_service = data_service

    def get_currency_exchange_rates(self, current_date):
        data = self.data_service.get_currency_data_by_date(current_date)
        response = {
            'data': data
        }
        return CurrencyInsightsResponse(response).format_ok()
