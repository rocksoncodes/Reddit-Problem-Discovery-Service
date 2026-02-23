from services.sentiment_service import SentimentService
from utils.logger import logger


def execute_sentiment_pipeline():
    try:
        logger.info("===Starting sentiment pipeline ===")
        processor = SentimentService()
        processor.query_posts_with_comments()
        processor.analyze_post_sentiment()
        processor.summarize_post_sentiment()
        processor.store_sentiment_results()
        logger.info("=== Sentiment pipeline completed successfully ===")
        return True

    except Exception as e:
        logger.error(f"Error in sentiment pipeline: {e}", exc_info=True)
        return {"error": str(e)}
