import psycopg2

def init_db():
    db_name = "ProjectAS_DB"
    db_user = "rooot"
    db_password = "smart"
    db_host = "localhost"
    db_port = 5432

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
        print(f"База данных '{db_name}' успешно создана.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")

if __name__ == "__main__":
    init_db()
