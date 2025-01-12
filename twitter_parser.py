import os
import tweepy
import json
import uuid
import logging
from datetime import datetime
import pytz
from config import TWITTER_CONFIG, TWITTER_ACCOUNTS, DATA_DIR, LOG_DIR, LOG_FILE

# Set up logging
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterParser:
    def __init__(self):
        self._setup_twitter_client()
        self.accounts = TWITTER_ACCOUNTS
        self.ist_tz = pytz.timezone('Asia/Kolkata')
        os.makedirs(DATA_DIR, exist_ok=True)
        
    def _setup_twitter_client(self):
        """Setup Twitter API client with error handling"""
        try:
            self.client = tweepy.Client(
                bearer_token=TWITTER_CONFIG['BEARER_TOKEN'],
                consumer_key=TWITTER_CONFIG['API_KEY'],
                consumer_secret=TWITTER_CONFIG['API_SECRET'],
                access_token=TWITTER_CONFIG['ACCESS_TOKEN'],
                access_token_secret=TWITTER_CONFIG['ACCESS_TOKEN_SECRET'],
                wait_on_rate_limit=True
            )
            logger.info("Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {str(e)}")
            raise

    def initialize_account_ids(self):
        """Initialize Twitter IDs for all monitored accounts"""
        for username in self.accounts.keys():
            try:
                user_id = self.get_user_id(username)
                if user_id:
                    self.accounts[username] = user_id
                    logger.info(f"Retrieved ID for {username}: {user_id}")
                else:
                    logger.error(f"Could not retrieve ID for {username}")
            except Exception as e:
                logger.error(f"Error initializing account ID for {username}: {str(e)}")

    def get_user_id(self, username):
        """Get Twitter user ID from username"""
        try:
            user = self.client.get_user(username=username)
            return user.data.id
        except Exception as e:
            logger.error(f"Error getting user ID for {username}: {str(e)}")
            return None

    def format_tweet(self, tweet, author):
        """Format tweet data according to required structure"""
        current_time = datetime.now(self.ist_tz)
        
        return {
            "id": hash(tweet.id),  # Using hash of tweet ID as unique identifier
            "created_at": current_time.isoformat(),
            "updated_at": current_time.isoformat(),
            "reference_id": str(uuid.uuid4()),
            "title": tweet.text[:100] + "..." if len(tweet.text) > 100 else tweet.text,
            "author": author,
            "url": f"https://twitter.com/{author}/status/{tweet.id}",
            "hostname": "twitter.com",
            "description": tweet.text,
            "crawled_at": current_time.isoformat(),
            "published_at": tweet.created_at.astimezone(self.ist_tz).isoformat(),
            "categories": "Markets",
            "stocks": [],
            "classes": [],
            "indices": [],
            "stock_names": [],
            "summary": None,
            "companies": [],
            "sentiment": None
        }

    def fetch_latest_tweets(self):
        """Fetch latest tweets from monitored accounts"""
        all_tweets = []
        
        for username, user_id in self.accounts.items():
            try:
                tweets = self.client.get_users_tweets(
                    id=user_id,
                    max_results=10,
                    tweet_fields=['created_at', 'text']
                )
                
                if tweets.data:
                    for tweet in tweets.data:
                        formatted_tweet = self.format_tweet(tweet, username)
                        all_tweets.append(formatted_tweet)
                        
            except Exception as e:
                logger.error(f"Error fetching tweets for {username}: {str(e)}")
                continue
                
        return all_tweets

    def start_stream(self):
        """Initialize stream listener for real-time updates"""
        rules = [
            tweepy.StreamRule(f"from:{username}") 
            for username in self.accounts.keys()
        ]
        
        stream = tweepy.StreamingClient(
            bearer_token=TWITTER_CONFIG['BEARER_TOKEN'],
            wait_on_rate_limit=True
        )
        
        # Add rules
        for rule in rules:
            try:
                stream.add_rules(rule)
            except Exception as e:
                logger.error(f"Error adding rule: {str(e)}")
                
        return stream

if __name__ == "__main__":
    parser = TwitterParser()
    parser.initialize_account_ids()
    
    # First, get historical tweets
    historical_tweets = parser.fetch_latest_tweets()
    logger.info(f"Fetched {len(historical_tweets)} historical tweets")
    
    # Start streaming for real-time updates
    stream = parser.start_stream()
    logger.info("Started streaming real-time tweets...")
