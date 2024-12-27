import subprocess
import sys

def install_libraries():
    libraries = [
        "fastapi",
        "sqlalchemy",
        "psycopg2",
        "alembic",
        "uvicorn"
    ]
    for library in libraries:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

if __name__ == "__main__":
    install_libraries()
