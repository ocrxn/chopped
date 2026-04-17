import os
import sys
from dotenv import load_dotenv
import logging

load_dotenv()

if hasattr(sys, '_MEIPASS'):
    env_path = os.path.join(sys._MEIPASS, '.env')
    logging.info(f"Looking for .env at: {env_path}")
    logging.info(f".env exists: {os.path.exists(env_path)}")
    load_dotenv(env_path)
else:
    load_dotenv()

logging.info(f"DATABASE_URL loaded: {bool(os.getenv('DATABASE_URL'))}")
logging.info(f"APP_KEY loaded: {bool(os.getenv('APP_KEY'))}")


# Base directory
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Neon DB
DATABASE_URL = os.getenv('DATABASE_URL')

# Uploads & output
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
JSON_FOLDER = os.path.join(BASE_DIR, "json")
CLIPS_FOLDER = os.path.join(BASE_DIR, "clips")
ZIP_FOLDER = os.path.join(BASE_DIR, "zips")

for folder in [UPLOAD_FOLDER, JSON_FOLDER, CLIPS_FOLDER, ZIP_FOLDER]:
    os.makedirs(folder, exist_ok=True)