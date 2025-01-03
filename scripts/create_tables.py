from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:smart@localhost/ProjectAS_DB"  # Заменен пользователь
engine = create_engine(DATABASE_URL)
