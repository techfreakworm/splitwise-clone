import sys
import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    DB_ENDPOINT=os.getenv('DB_ENDPOINT')