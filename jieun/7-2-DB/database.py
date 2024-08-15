from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import get_settings
from typing import Generator

settings = get_settings()

DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    settings.MYSQL_USER,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_HOST,
    settings.MYSQL_PORT,
    settings.MYSQL_DATABASE
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()