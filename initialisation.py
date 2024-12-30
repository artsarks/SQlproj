import psycopg2

DATABASE = "ProjectAS_DB"
USER = "postgres"
PASSWORD = "smartbOb"
HOST = "localhost"
PORT = 5432

def init_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE {DATABASE} OWNER {USER};")
        print(f"База данных {DATABASE} успешно создана!")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()
