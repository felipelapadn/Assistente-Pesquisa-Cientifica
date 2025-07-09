FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y build-essential \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
