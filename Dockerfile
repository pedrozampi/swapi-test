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
    MONGO_PASSWORD=NEKncn92728 \
    MONGO_HOST=node257373-swapi.sp1.br.saveincloud.net.br \
    MONGO_PORT=27017 \
    MONGO_URI=mongodb+srv://PedroZ:pwd123pwd@cluster0.rwdhmgd.mongodb.net/starwars?authSource=admin \
    REDIS_URL=redis://default:xxtrdLmkp9QQGOoEL5t5ES48Xc1Jnaow@redis-16744.c336.samerica-east1-1.gce.cloud.redislabs.com:16744

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
