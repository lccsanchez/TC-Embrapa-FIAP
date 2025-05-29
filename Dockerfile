FROM python:3.11.9 AS builder

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Rode os testes no build
RUN pytest

# Produção
FROM python:3.11.9
WORKDIR /app
COPY --from=builder /app /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
