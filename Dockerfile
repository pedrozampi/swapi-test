FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BASE_URL=https://swapi.dev/api/ \
    SECRET_KEY=sW4p1* \
    ALGORITHM=HS256 \
    ACCESS_TOKEN_EXPIRE_MINUTES=30 \
    MONGO_DB=starwars \
    MONGO_USERNAME=admin \
    MONGO_PASSWORD=admin123 \
    MONGO_HOST=mongodb \
    MONGO_PORT=27017 \
    REDIS_URL=redis://redis:6379

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
