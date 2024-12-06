from sqlalchemy_utils import create_database, database_exists
from urllib.parse import urlparse


def create_database_automatically(database_url: str) -> None:
    """Creates a SQLAlchemy database if it does not already exist.

    Args:
        database_url (str): URL of the SQLAlchemy database
    """
    parsed_url = urlparse(database_url)
    db_name = parsed_url.path.lstrip('/')
    
    if not database_exists(database_url):
        create_database(database_url)
        print(f"Database {db_name} created successfully.")
    #else:
    #    print(f"Database {db_name} already exists and create_database_automatically utils run successfully.")
