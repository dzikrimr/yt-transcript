# Gunakan base image Python yang lebih lengkap untuk kemudahan instalasi
FROM python:3.9

# Set direktori kerja
WORKDIR /app

# Install ffmpeg, sebuah dependency penting untuk Whisper
RUN apt-get update && apt-get install -y ffmpeg

# Salin dan install library Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa kode aplikasi
COPY . .

# Expose port dan jalankan server
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "main:app"]