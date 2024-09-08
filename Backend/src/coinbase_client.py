from coinbase.wallet.client import Client
from src.config import Config

class CoinbaseClient:
    def __init__(self):
        self.client = Client(Config.COINBASE_API_KEY, Config.COINBASE_API_SECRET)
        self.base_url = 'https://api.coinbase.com/v2'

    def get_account_balance(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{self.base_url}/accounts', headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Extract balance from the response; adjust based on your API response structure
            return data['data'][0]['balance']['amount']
        else:
            return 'Error retrieving balance'
