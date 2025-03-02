"""
Telegram Bot Module

This module provides functionality to interact with the Telegram Bot API. It allows sending messages
to a specified chat using a bot token and chat ID. The module is designed to be simple and reusable.

Author: Sean Le Cornu
Date: 2025-03-02
Version: 1.0
"""

import os
import requests
from src.deribit import DeribitAPI, DERIBIT_API_KEY, DERIBIT_API_SECRET

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat using the Telegram Bot API.

    :param bot_token: Your Telegram bot's API token.
    :param message: The message to send.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to send message: {e}") from e


deribit_client = DeribitAPI(DERIBIT_API_KEY, DERIBIT_API_SECRET)
BTC_price = deribit_client.get_public_data("btc_usd")["result"]["index_price"]

send_telegram_message(BOT_TOKEN, CHAT_ID,
                      "Hello Sean, the price of Bitcoin this morning is: "
                      + str(round(BTC_price,1)) )
