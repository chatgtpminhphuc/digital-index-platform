import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
