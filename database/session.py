from sqlalchemy.orm import sessionmaker
from database.engine import database_engine

# ==============================================================================================
# To avoid circular imports, this file contains utility functions used across multiple modules.
# ==============================================================================================


def get_session():
    session_make = sessionmaker(bind=database_engine)
    session = session_make()
    return session
