# Базовый образ
FROM python:3.12-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Команда запуска
CMD ["gunicorn", "--bind", "213.171.10.209:1000", "config.wsgi:application"]