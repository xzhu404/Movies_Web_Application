"""Flask configuration variables."""
import os
from os import environ
from dotenv import load_dotenv

# Load environment variables from file .env, stored in this directory.
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')