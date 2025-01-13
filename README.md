# Social Media Parser

This module fetches real-time updates from Twitter and Telegram channels and formats them according to our data structure.

## Setup Instructions

1. **Twitter Setup**:
   - Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Sign up for a developer account
   - Create a new Project and App
   - Get your API credentials (Bearer Token, API Key & Secret, Access Token & Secret)

2. **Telegram Setup**:
   - Go to [Telegram API Development Tools](https://my.telegram.org/apps)
   - Log in with your phone number
   - Create a new application to get API credentials
   - Note down your API ID and API Hash

3. **Environment Setup**:
   Create a `.env` file in the root directory with your credentials:
   ```
   # Twitter Credentials
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   TWITTER_API_KEY=your_api_key_here
   TWITTER_API_SECRET=your_api_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here

   # Telegram Credentials
   TELEGRAM_API_ID=your_api_id_here
   TELEGRAM_API_HASH=your_api_hash_here
   TELEGRAM_PHONE=your_phone_number_here
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Channels**:
   Edit `config.py` to add your Telegram channel names/links

6. **Run the Parser**:
   ```bash
   python main.py
   ```

## Features

- Real-time monitoring of Twitter and Telegram channels
- Unified data structure for both platforms
- Automatic data persistence
- Comprehensive logging system
- Error handling and recovery
- Rate limiting compliance

## Monitored Sources


## Data Structure

All messages are stored in the following format:
```json
{
    "id": "unique_id",
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp",
    "reference_id": "UUID",
    "title": "Message title/preview",
    "author": "Channel/Account name",
    "url": "Original post URL",
    "hostname": "Platform domain",
    "description": "Full message content",
    "crawled_at": "ISO timestamp",
    "published_at": "ISO timestamp",
    "categories": "Markets",
    "stocks": [],
    "classes": [],
    "indices": [],
    "stock_names": [],
    "summary": null,
    "companies": [],
    "sentiment": null
}
```

## Troubleshooting

- Check `logs/parser.log` for detailed error messages
- Ensure all API credentials are correct
- Verify channel/account names exist and are accessible
- Check network connectivity
