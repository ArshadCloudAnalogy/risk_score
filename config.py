import os

QUILTT_API_KEY = os.getenv("QUILTT_API_KEY", "replace-me")        # Quiltt secret API key
QUILTT_BASE_URL = os.getenv("QUILTT_BASE_URL", "https://api.quiltt.io")
QUILTT_WEBHOOK_SECRET = os.getenv("QUILTT_WEBHOOK_SECRET", "replace-me")  # for HMAC verification
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")      # for redirect/callback if needed
