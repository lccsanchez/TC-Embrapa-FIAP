FROM python:3.11

# Instala dependências do sistema e ODBC Driver 18
RUN apt-get update && \
    apt-get install -y curl gnupg2 ca-certificates && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn app.main:app --bind=0.0.0.0:$PORT