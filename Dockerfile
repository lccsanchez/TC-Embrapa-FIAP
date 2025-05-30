# Multi-stage build para rodar testes e deploy
FROM python:3.11.9-slim AS builder

WORKDIR /app

# Instala dependências do sistema se necessário
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências primeiro (para melhor cache)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação E os testes
COPY . .

# Roda os testes - se falharem, a build para aqui
RUN pytest tests/ --maxfail=1 --disable-warnings -v

# Estágio de produção (só executa se os testes passarem)
FROM python:3.11.9-slim AS production

WORKDIR /app

# Instala dependências mínimas para produção
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements.txt
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas os arquivos necessários para produção do builder
COPY --from=builder /app/app ./app
COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/alembic.ini ./
COPY --from=builder /app/certs ./certs

# Cria usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Comando para rodar a aplicação
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
