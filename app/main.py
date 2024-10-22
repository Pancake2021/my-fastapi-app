import os
import psycopg2
from fastapi import FastAPI
from psycopg2 import sql

app = FastAPI()

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

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_main():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM test_table;')
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"test_counter": count}
