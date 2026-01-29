from pipelines.egress_pipeline import execute_egress_pipeline
from config import settings

notion_only = settings.CHOICE_ONE
email_only = settings.CHOICE_TWO
all_channels = settings.CHOICE_THREE

if __name__ == "__main__":
    execute_egress_pipeline(all_channels)
