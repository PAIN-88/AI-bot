FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python ingest.py

EXPOSE 7860

CMD ["python", "main.py"]