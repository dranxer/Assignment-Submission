FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run database migrations and start server
CMD ["sh", "-c", "python -c 'from app.database import init_db; init_db()' && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"]
