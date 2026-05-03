FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH="/app/src"

# Copiamos requirements.txt
COPY requirements.txt .

# Instalamos todas las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY src/ ./src/
COPY tests/ ./tests/

CMD ["uvicorn", "gtc_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
