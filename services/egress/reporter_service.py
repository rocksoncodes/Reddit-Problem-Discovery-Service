from notion_client import APIErrorCode, APIResponseError, Client
from sqlalchemy.orm import sessionmaker
from database.engine import database_engine
from database.session import get_session
from database.models import ProcessedBriefs
from utils.logger import logger
from config import settings

Session = sessionmaker(bind=database_engine)

class ReporterService:
    def __init__(self):
        self.queried_briefs = []
        self.notion_key = settings.NOTION_API_KEY
        self.notion_parent_page = settings.NOTION_DB_ID
        self.notion_client = Client(auth=self.notion_key)
        self.session = get_session()


    def query_briefs(self) -> list[dict] | None:
        try:
            session = self.session
            queried_briefs = session.query(ProcessedBriefs).all()
            queries = []

            if not queried_briefs:
                raise ValueError("No briefs found in the database.")

            for brief in queried_briefs:
                query_results = {
                    "id": brief.id,
                    "curated_content" : brief.curated_content
                }
                queries.append(query_results)


            logger.info("Successfully queried briefs from the database.")
            self.queried_briefs = queries
            return queries

        except Exception as e:
            logger.error(f"Error querying briefs from the database!:{e}",exc_info=True)
            return None


    def create_notion_page(self):

        content = self.queried_briefs

        if not content:
            self.query_briefs()
            logger.info("No content to publish to Notion. Calling query_briefs().")
            content = self.queried_briefs

        try:
            response = self.notion_client.pages.create(
                parent={"page_id": self.notion_parent_page},

                properties = {
                    "title": [
                        {
                            "type":"text",
                            "text":{"content":"My Reddit Report"}
                        }
                    ]
                },

                children = [
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [
                                {"type": "text", "text": {"content":"Project Proposals"}}
                            ]
                        }
                    },
                    {
                        "object":"block",
                        "type":"paragraph",
                        "paragraph":{
                            "rich_text":[
                                {"type":"text","text":{"content":content[0].get("curated_content")}}
                            ]
                        }
                    }
                ]
            )

            logger.info("Notion page created successfully.")
            print(response)

        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                logger.error("The specified parent page was not found.", exc_info=True)
            else:
                logger.error(f"An error occurred while creating the Notion page:", exc_info=True)