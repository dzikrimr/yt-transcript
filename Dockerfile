# Gunakan base image Python yang ringan dan resmi
FROM python:3.9-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements terlebih dahulu untuk optimasi cache Docker
COPY requirements.txt .

# Install semua library yang dibutuhkan, nonaktifkan cache untuk menjaga ukuran image tetap kecil
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa kode aplikasi Anda (main.py) ke dalam direktori kerja
COPY . .

# Beri tahu Docker bahwa container akan berjalan di port 8000
EXPOSE 8000

# Perintah untuk menjalankan aplikasi menggunakan Gunicorn saat container dimulai
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]