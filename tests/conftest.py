import pytest
import os
from dotenv import load_dotenv
from ClockifyUpdater import ClockifyUpdater
from NotionParser import Parser

dotenv_path = os.path.join(os.pardir, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
CLOCKIFY_TOKEN = os.getenv("CLOCKIFY_TOKEN")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
CLOCKIFY_USER_ID = os.getenv("CLOCKIFY_USER_ID")


@pytest.fixture
def connect():
    return Parser(NOTION_TOKEN), ClockifyUpdater(CLOCKIFY_TOKEN,
                                                 CLOCKIFY_WORKSPACE_ID,
                                                 CLOCKIFY_USER_ID)
