from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 👇 Replace with your real MySQL credentials
DATABASE_URL = "mysql+pymysql://root:root_123@localhost:3306/secure_file_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
