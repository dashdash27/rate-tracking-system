import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в переменных окружения или .env файле!")

engine = create_engine(DATABASE_URL, client_encoding='utf8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)