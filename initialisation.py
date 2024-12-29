import paramiko
import psycopg2
from psycopg2 import sql

ssh_host = "83.149.198.142"
ssh_port = 22
ssh_user = "user5448"
ssh_password = "BVn6i1U3fM5Vp"

db_host = "localhost"
db_port = 5432
db_user = "postgres"
db_password = "smartbOb"
new_db_name = "auto_workshop"
new_db_owner = "workshop_owner"

try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

    transport = ssh_client.get_transport()
    tunnel = transport.open_channel("direct-tcpip", (db_host, db_port), ("127.0.0.1", 0))

    connection = psycopg2.connect(
        host="localhost",
        port=db_port,
        user=db_user,
        password=db_password,
        database="postgres",
        connection_factory=lambda: tunnel
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(sql.SQL("CREATE ROLE {owner} WITH LOGIN PASSWORD 'owner_password';")
                   .format(owner=sql.Identifier(new_db_owner)))
    cursor.execute(sql.SQL("CREATE DATABASE {db_name} OWNER {owner};")
                   .format(db_name=sql.Identifier(new_db_name),
                           owner=sql.Identifier(new_db_owner)))

    print(f"База данных '{new_db_name}' создана с владельцем '{new_db_owner}'")

except Exception as e:
    print("Ошибка:", e)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
    if 'ssh_client' in locals():
        ssh_client.close()
