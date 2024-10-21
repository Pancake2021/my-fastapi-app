from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# Инициализация метрики
test_counter = Counter('test_counter', 'Number of delete requests to /delete_number')

# Настройки подключения к базе данных из переменных окружения
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'test_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Инициализация базы данных
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS numbers (
            id SERIAL PRIMARY KEY,
            value INTEGER NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.delete("/delete_number/{number_id}")
def delete_number(number_id: int):
    test_counter.inc()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM numbers WHERE id = %s RETURNING *;", (number_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return {"message": f"Number with id {number_id} deleted."}
    else:
        raise HTTPException(status_code=404, detail="Number not found")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def read_root():
    return {"test_counter": test_counter._value.get()}

# Временный эндпоинт для добавления числа
@app.post("/add_number/{value}")
def add_number(value: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO numbers (value) VALUES (%s) RETURNING id;", (value,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "value": value}

