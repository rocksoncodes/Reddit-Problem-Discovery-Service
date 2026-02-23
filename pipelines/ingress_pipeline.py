from database.init_db import init_db
from handlers.reddit_handler import scrape_reddit_data, store_reddit_data
from pipelines.sentiment_pipeline import execute_sentiment_pipeline
from utils.logger import logger


def run_ingress_pipeline():
    try:
        logger.info("=== Starting Egress pipeline ===")
        init_db()
        reddit_data = scrape_reddit_data()
        store_reddit_data(reddit_data)
        execute_sentiment_pipeline()
        logger.info("=== Ingress pipeline completed successfully ===")
        return True

    except Exception as e:
        logger.error("Error executing Ingress pipeline:", exc_info=True)
        return {"error": str(e)}
