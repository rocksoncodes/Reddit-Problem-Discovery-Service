from services.egress.reporter_service import ReporterService

execute = ReporterService()

if __name__ == "__main__":
    execute.query_briefs()
    execute.create_notion_page()