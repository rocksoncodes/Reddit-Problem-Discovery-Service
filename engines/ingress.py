from database.init_db import init_db
from handlers.reddit_handler import scrape_reddit_data, store_reddit_data
from pipelines.sentiment_pipeline import execute_sentiment_pipeline

def run_reddit_ingest():
    init_db()
    reddit_data = scrape_reddit_data()
    store_reddit_data(reddit_data)
    execute_sentiment_pipeline()

if __name__ == "__main__":
    run_reddit_ingest()