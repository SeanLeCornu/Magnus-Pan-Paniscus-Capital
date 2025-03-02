import requests
import hmac
import hashlib
import time
import json
import os


# Deribit API credentials
DERIBIT_API_KEY = os.getenv("DERIBIT_API_KEY")
DERIBIT_API_SECRET = os.getenv("DERIBIT_API_SECRET")
BASE_URL = "https://deribit.com/api/v2"

def deribit_generate_signature(secret, params):
    """Generate HMAC signature for authentication."""
    return hmac.new(
        secret.encode('utf-8'),
        params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def deribit_get_public_data(index):
    endpoint = f"{BASE_URL}/public/get_index_price"
    params = {
        "index_name": index
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def deribit_get_account_summary(currency="BTC"):
    """Fetch account summary for a specific currency (BTC or ETH)."""
    endpoint = f"{BASE_URL}/private/get_account_summary"

    # Required parameters
    params = {
        "currency": currency,  # Can be "BTC" or "ETH"
        "nonce": str(int(time.time() * 1000))  # Unique nonce
    }

    # Generate signature
    params['sig'] = deribit_generate_signature(
        DERIBIT_API_SECRET,
        f"{params['nonce']}{params['currency']}"
    )

    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {DERIBIT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None



# Example usage
if __name__ == "__main__":
    data = deribit_get_public_data("btc_usd")["result"]["index_price"]
    print(json.dumps(data, indent=2))

    account_summary = deribit_get_account_summary(currency="BTC")
    print("Account Summary:", account_summary)

   # print(json.dumps(account_summary, indent=2))

  #  result = account_summary.get("result", {})
  #  print("\nKey Details:")
  #  print(f"Balance: {result.get('balance', 'N/A')} BTC")
  #  print(f"Available Funds: {result.get('available_funds', 'N/A')} BTC")
  #  print(f"Equity: {result.get('equity', 'N/A')} BTC")
  #  print(f"Initial Margin: {result.get('initial_margin', 'N/A')} BTC")
  #  print(f"Maintenance Margin: {result.get('maintenance_margin', 'N/A')} BTC")



