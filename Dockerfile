# =============================
# Etapa 1: Build e Teste
# =============================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements-dev.txt

COPY . .

# Carrega .env se existir e roda testes
RUN set -a && \
    [ -f .env ] && . .env || echo "No .env found" && \
    set +a && \
    pytest --maxfail=1 --disable-warnings --tb=short

# =============================
# Etapa 2: Imagem Final
# =============================
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

# Comando para rodar a aplicação
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
