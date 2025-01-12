import os
import json
import uuid
import logging
from datetime import datetime
import pytz
from telethon import TelegramClient, events
from telethon.tl.types import Channel
from config import TELEGRAM_CONFIG, TELEGRAM_CHANNELS, DATA_DIR, LOG_DIR, LOG_FILE, TELEGRAM_FILE

# Set up logging
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramParser:
    def __init__(self):
        self._setup_client()
        self.ist_tz = pytz.timezone('Asia/Kolkata')
        os.makedirs(DATA_DIR, exist_ok=True)

    async def _setup_client(self):
        """Initialize Telegram client with error handling"""
        try:
            self.client = TelegramClient(
                'market_news_session',
                TELEGRAM_CONFIG['API_ID'],
                TELEGRAM_CONFIG['API_HASH']
            )
            await self.client.start(phone=TELEGRAM_CONFIG['PHONE'])
            logger.info("Telegram client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Telegram client: {str(e)}")
            raise

    def format_message(self, message, channel_name):
        """Format Telegram message according to required structure"""
        current_time = datetime.now(self.ist_tz)
        
        return {
            "id": hash(f"{channel_name}_{message.id}"),
            "created_at": current_time.isoformat(),
            "updated_at": current_time.isoformat(),
            "reference_id": str(uuid.uuid4()),
            "title": message.message[:100] + "..." if len(message.message) > 100 else message.message,
            "author": channel_name,
            "url": f"https://t.me/{channel_name}/{message.id}",
            "hostname": "telegram.org",
            "description": message.message,
            "crawled_at": current_time.isoformat(),
            "published_at": message.date.astimezone(self.ist_tz).isoformat(),
            "categories": "Markets",
            "stocks": [],
            "classes": [],
            "indices": [],
            "stock_names": [],
            "summary": None,
            "companies": [],
            "sentiment": None
        }

    async def save_message(self, formatted_message):
        """Save formatted message to file"""
        try:
            existing_messages = []
            if os.path.exists(TELEGRAM_FILE):
                with open(TELEGRAM_FILE, 'r', encoding='utf-8') as f:
                    existing_messages = json.load(f)
            
            existing_messages.append(formatted_message)
            
            with open(TELEGRAM_FILE, 'w', encoding='utf-8') as f:
                json.dump(existing_messages, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved message {formatted_message['id']} to file")
        except Exception as e:
            logger.error(f"Error saving message to file: {str(e)}")

    async def process_new_message(self, event):
        """Process new messages from channels"""
        try:
            channel = await event.get_chat()
            if isinstance(channel, Channel):
                formatted_message = self.format_message(event.message, channel.username)
                await self.save_message(formatted_message)
                logger.info(f"Processed new message from {channel.username}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    async def start_monitoring(self):
        """Start monitoring Telegram channels"""
        try:
            for channel in TELEGRAM_CHANNELS:
                self.client.add_event_handler(
                    self.process_new_message,
                    events.NewMessage(chats=channel)
                )
            
            logger.info("Started monitoring Telegram channels")
            await self.client.run_until_disconnected()
        except Exception as e:
            logger.error(f"Error in monitoring: {str(e)}")

if __name__ == "__main__":
    parser = TelegramParser()
    import asyncio
    asyncio.run(parser.start_monitoring())
