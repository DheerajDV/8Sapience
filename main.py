import asyncio
import logging
from twitter_parser import TwitterParser
from telegram_parser import TelegramParser
from config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize parsers
        twitter_parser = TwitterParser()
        telegram_parser = TelegramParser()

        # Start Twitter parser in a separate task
        twitter_task = asyncio.create_task(
            asyncio.to_thread(twitter_parser.start_stream)
        )

        # Start Telegram parser
        telegram_task = asyncio.create_task(
            telegram_parser.start_monitoring()
        )

        # Wait for both tasks
        await asyncio.gather(twitter_task, telegram_task)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
