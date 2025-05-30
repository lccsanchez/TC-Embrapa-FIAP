# =============================
# Etapa 1: Build e Teste
# =============================
FROM python:3.11.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Carrega .env se existir e roda testes
RUN set -a && \
    [ -f .env ] && . .env || echo "No .env found" && \
    set +a && \
    pytest --maxfail=1 --disable-warnings --tb=short

# =============================
# Etapa 2: Imagem Final
# =============================
FROM python:3.11.9-slim AS production

WORKDIR /app

# Instala dependências mínimas do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements.txt
COPY requirements.txt ./

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas arquivos necessários para produção
COPY --from=builder /app/app ./app
COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/alembic.ini ./
COPY --from=builder /app/certs ./certs

# Cria usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Comando para rodar a aplicação
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
