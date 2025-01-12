import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API Configuration
TWITTER_CONFIG = {
    'BEARER_TOKEN': os.getenv('TWITTER_BEARER_TOKEN'),
    'API_KEY': os.getenv('TWITTER_API_KEY'),
    'API_SECRET': os.getenv('TWITTER_API_SECRET'),
    'ACCESS_TOKEN': os.getenv('TWITTER_ACCESS_TOKEN'),
    'ACCESS_TOKEN_SECRET': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
}

# Twitter Accounts to Monitor
TWITTER_ACCOUNTS = {
    'ETMarkets': None,  # Will be populated with actual ID
    'Breakoutrade94': None,
    'Trading4Bucks': None
}

# Telegram Configuration
TELEGRAM_CONFIG = {
    'API_ID': os.getenv('TELEGRAM_API_ID'),
    'API_HASH': os.getenv('TELEGRAM_API_HASH'),
    'BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
    'PHONE': os.getenv('TELEGRAM_PHONE')
}

# Telegram Channels to Monitor
TELEGRAM_CHANNELS = [
    'channel_1',  # Replace with actual channel names/links
    'channel_2',
    'channel_3'
]

# Data Storage Configuration
DATA_DIR = 'data'
TWEETS_FILE = os.path.join(DATA_DIR, 'tweets.json')
TELEGRAM_FILE = os.path.join(DATA_DIR, 'telegram.json')

# Logging Configuration
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'parser.log')

# Common Settings
BATCH_SIZE = 100
UPDATE_INTERVAL = 60  # seconds
