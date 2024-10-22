import os
import psycopg2
from fastapi import FastAPI
from contextlib import asynccontextmanager

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'test_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            value INTEGER NOT NULL
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    init_db()
    yield
    # Код, выполняемый при остановке приложения (если необходимо)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_main():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM test_table;')
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"test_counter": count}
