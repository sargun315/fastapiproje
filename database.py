from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:sargun@localhost:5432/blogdb"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("PostgreSQL connected successfully!")
except Exception as e:
    print("Connection failed:")
    print(e)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()