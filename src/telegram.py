"""
Telegram Bot Module

This module provides functionality to interact with the Telegram Bot API. It allows sending messages
to a specified chat using a bot token and chat ID. The module is designed to be simple and reusable.
"""

import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat using the Telegram Bot API.

    :param bot_token: Your Telegram bot's API token.
    :param chat_id: The chat ID of the recipient.
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
        raise Exception(f"Failed to send message: {e}")

send_telegram_message(BOT_TOKEN, CHAT_ID, "Hello World!")
