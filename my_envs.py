import os
from dotenv import find_dotenv, load_dotenv

def load_config():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    # Corrected environment variable assignments
    HBNB_ENV = os.getenv("HBNB_ENV")
    HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
    HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
    HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
    HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")
    HBNB_TYPE_STORAGE = os.getenv("HBNB_TYPE_STORAGE")

    return HBNB_ENV, HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB, HBNB_TYPE_STORAGE
