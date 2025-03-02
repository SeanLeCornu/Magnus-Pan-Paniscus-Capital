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
import hmac
import hashlib
import time
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
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _generate_signature(self, params):
        """Generate HMAC signature for authentication."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def get_public_data(self, index):
        """Fetch public data (e.g., index price) from Deribit."""
        endpoint = f"{self.base_url}/public/get_index_price"
        params = {
            "index_name": index
        }

        response = requests.get(endpoint, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        print(f"Error: {response.status_code}")
        return None

    def get_account_summary(self, currency="BTC"):
        """Fetch account summary for a specific currency (BTC or ETH)."""
        endpoint = f"{self.base_url}/private/get_account_summary"

        # Required parameters
        params = {
            "currency": currency,  # Can be "BTC" or "ETH"
            "nonce": str(int(time.time() * 1000))  # Unique nonce
        }

        # Generate signature
        params['sig'] = self._generate_signature(
            f"{params['nonce']}{params['currency']}"
        )

        # Headers for authentication
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Make the API request
        response = requests.get(endpoint, headers=headers, params=params, timeout=5)

        if response.status_code == 200:
            return response.json()
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


# Example Usage
if __name__ == "__main__":
    deribit_client = DeribitAPI(DERIBIT_API_KEY, DERIBIT_API_SECRET)
    index_price_data = deribit_client.get_public_data("btc_usd")["result"]["index_price"]
    print("Index Price Data:", index_price_data)

    account_summary = deribit_client.get_account_summary("BTC")
    print("Account Summary:", account_summary)
