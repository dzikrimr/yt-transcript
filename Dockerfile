# Gunakan Python versi 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode server
COPY . .

# Expose port (Railway akan gunakan PORT environment variable)
EXPOSE 8000

# Jalankan FastAPI dengan uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
