"""
Deribit API Module

A Python module for interacting with the Deribit API. This module provides a class
to handle authentication, fetch public data (e.g., index prices), and retrieve
account summaries for authenticated users.

Author: Sean Le Cornu
Date: 2025-03-02
Version: 1.0
"""

import os
import requests

# Deribit API credentials
BASE_URL = "https://deribit.com/api/v2"
DERIBIT_API_KEY = os.getenv("DERIBIT_API_KEY")
DERIBIT_API_SECRET = os.getenv("DERIBIT_API_SECRET")

class DeribitAPI:
    """
    A class to interact with the Deribit API.

    Attributes:
        api_key (str): The API key for Deribit authentication.
        api_secret (str): The API secret for Deribit authentication.
        base_url (str): The base URL for the Deribit API (default is v2).

    Methods:
        get_public_data(index): Fetches public data (e.g., index price) for a given index.
        get_account_summary(currency): Retrieves the account summary for a specific currency.
        _generate_signature(params): Generates an HMAC signature for authentication.
    """

    def __init__(self, api_key, api_secret, base_url=BASE_URL):
        """Initialize the DeribitAPI class with API credentials."""
        if not api_key or not api_secret:
            raise ValueError("API key and secret must be provided.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.access_token = self.authenticate()

    def authenticate(self):
        """Authenticate with Deribit and obtain an OAuth2 access token."""
        endpoint = f"{self.base_url}/public/auth"
        params = {
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "grant_type": "client_credentials"
        }

        try:
            auth_resp = requests.get(endpoint, params=params, timeout=10)
            auth_data = auth_resp.json()
            self.access_token = auth_data["result"]["access_token"]
        except requests.exceptions.Timeout as e:
            print(f"Request timed out: {e}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        return self.access_token

    def get_public_data(self, index):
        """Fetch public data from Deribit."""
        endpoint = f"{self.base_url}/public/get_index_price"
        params = {
            "index_name": index
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if "result" in data:
                return data["result"]
            print("Error: Unexpected response format")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_account_balance(self, currency):
        """Fetch account balance for a specific currency. Private end points need www. added..."""
        endpoint = (f"{self.base_url[:8]}www.{self.base_url[8:]}"
                    f"/private/get_account_summary?currency={currency}")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        resp = requests.get(endpoint, headers=headers, timeout=10)
        data = resp.json()
        return data["result"]['equity']

# Test Usage
if __name__ == "__main__":
    deribit_client = DeribitAPI(DERIBIT_API_KEY, DERIBIT_API_SECRET)
    # Current BTCUSD price
    index_price_data = deribit_client.get_public_data("btc_usd")["index_price"]
    print("BTC current price:", index_price_data)
    # Current account balance
    TOKEN = "USDT"
    balances = deribit_client.get_account_balance(currency=TOKEN)
    print({TOKEN}, " balance: ", balances)
