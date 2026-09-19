FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
# dev requirements are included because the seed script needs Faker
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY app ./app
COPY scripts ./scripts
ENV SALARY_DATABASE_URL=sqlite:////data/salary.db
VOLUME /data
EXPOSE 8000
# Seed only when the DB is empty (idempotent), then serve.
CMD ["sh", "-c", "python -m scripts.seed && uvicorn app.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8000}"]
