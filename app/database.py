from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://rooot:smart@localhost:5432/ProjectAS_DB"

# Обновите соединение с указанием новой схемы
engine = create_engine(DATABASE_URL, connect_args={"options": "-csearch_path=my_schema"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
