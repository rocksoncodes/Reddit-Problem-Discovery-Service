from services.core.curator_service import CuratorService
from utils.logger import logger


def execute_curator_pipeline():
    try:
        logger.info("=== Starting curator pipeline ===")

        execute = CuratorService()
        execute.execute_curator_agent()
        execute.store_curator_response()

        logger.info("=== Curator pipeline completed successfully ===")
        return True

    except Exception as e:
        logger.error("Error executing curator pipeline:", exc_info=True)
        return {"error": str(e)}