# ETAP 1: Budowanie (Builder)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY app/requirements.txt .

# Instalujemy zależności do konkretnego folderu
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# ETAP 2: Finalny obraz (Runtime)
FROM python:3.11-slim
WORKDIR /app

# Instalujemy libpq - to jest potrzebne dla PostgreSQL, żeby Python mógł z nim gadać
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY app/ .

ENV PATH=/root/.local/bin:$PATH
# Ważne: PYTHONUNBUFFERED sprawia, że logi w terminalu pojawiają się od razu
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]