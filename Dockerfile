FROM python:3.13-alpine

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONPATH=/app/src
CMD ["uvicorn", "registry:app", "--host", "0.0.0.0", "--port", "8080"]
