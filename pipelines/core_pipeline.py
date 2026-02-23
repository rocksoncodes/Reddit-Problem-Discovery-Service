from services.core_service import CoreService
from utils.logger import logger


def run_core_pipeline():
    try:
        logger.info("=== Starting curator pipeline ===")
        execute = CoreService()
        execute.execute_curator_agent()
        execute.store_curator_response()
        logger.info("=== Curator pipeline completed successfully ===")
        return True

    except Exception as e:
        logger.error("Error executing curator pipeline:", exc_info=True)
        return {"error": str(e)}
