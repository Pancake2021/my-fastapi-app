# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Указываем переменные окружения (можно также передавать их при запуске контейнера)
ENV DB_HOST=some-postgres
ENV DB_PORT=5432
ENV DB_NAME=test_db
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

