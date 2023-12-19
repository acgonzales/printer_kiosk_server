import os

from dotenv import load_dotenv

load_dotenv()

TEST_ENV = "test"
PROD_ENV = "prod"
ENV = os.getenv("ENV", TEST_ENV)
