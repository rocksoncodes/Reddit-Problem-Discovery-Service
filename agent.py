from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pipelines.egress_pipeline import run_egress_pipeline
from pipelines.core_pipeline import run_core_pipeline
from pipelines.ingress_pipeline import run_ingress_pipeline
from datetime import datetime, timedelta
from utils.logger import logger
from config import settings

notion_only = settings.CHOICE_ONE
email_only = settings.CHOICE_TWO
all_channels = settings.CHOICE_THREE


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BlockingScheduler(jobstores=jobstores)


def safe_run(function):
    def wrapper():
        try:
            logger.info(f"Running {function.__name__}")
            function()
            logger.info(f"Finished {function.__name__}")
        except Exception:
            logger.exception(f"Error running {function.__name__}")
    return wrapper


def run_all_pipelines():
    """
    Runs the pipelines synchronously in the correct order:
    Ingress -> Core -> Egress
    """
    logger.info("Starting full pipeline sequence")
    safe_run(run_ingress_pipeline)()
    safe_run(run_core_pipeline)()
    safe_run(lambda: run_egress_pipeline(all_channels))()
    logger.info("Full pipeline sequence finished")


# Schedule every 2 weeks
scheduler.add_job(
    run_all_pipelines,
    trigger="interval",
    weeks=2,
    next_run_time=datetime.now() + timedelta(seconds=10),
    id="full_pipeline_sequence",
    replace_existing=True
)

logger.info("Agent starting. Scheduler is now running...")
scheduler.start()
