FROM python:3.11.9

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --workers 1 --bind 0.0.0.0:$PORT
