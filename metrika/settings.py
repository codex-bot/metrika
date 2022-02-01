import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

URL = os.environ.get("URL")

APPLICATION_NAME = os.environ.get("APPLICATION_NAME")

SERVER = {
    'host': os.environ.get("SERVER_HOST"),
    'port': int(os.environ.get("SERVER_PORT"))
}

RABBITMQ = os.environ.get("RABBITMQ_HOST")

DB = {
    'name': os.environ.get("DATABASE_NAME"),
    'host': os.environ.get("DATABASE_HOST"),
    'port': int(os.environ.get("DATABASE_PORT"))
}

APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")

METRIKA_OAUTH_APP_ID = os.environ.get("METRIKA_OAUTH_APP_ID")
METRIKA_OAUTH_APP_SECRET = os.environ.get("METRIKA_OAUTH_APP_SECRET")

COLLECTIONS = {
    'tokens': os.environ.get("TOKENS_COLLECTION"),
    'counters': os.environ.get("COUNTERS_COLLECTION"),
    'schedulers': os.environ.get("SCHEDULERS_COLLECTION")
}
