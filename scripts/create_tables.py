from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:smart@localhost/ProjectAS_DB"  
engine = create_engine(DATABASE_URL)
