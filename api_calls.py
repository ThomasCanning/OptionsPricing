import requests


class ApiCalls:
    def __init__(self):
        self.alpha_vantage_api_key = '71JJZZ0D4J6HNGVD'

    # Queries the alpha-vantage API to get the latest 10-year US Treasury yield rate
    def get_us_treasury_yield(self):
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10year&apikey={self.alpha_vantage_api_key}'
        response = requests.get(url)
        data = response.json()

        latest_yield = float(data['data'][0]['value'])
        r = latest_yield / 100
        return r
