# Gunakan image dasar Python 3.10 (cukup stabil untuk Whisper)
FROM python:3.10-slim

# Instal dependensi sistem (ffmpeg dibutuhkan oleh whisper & yt_dlp)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Buat folder kerja
WORKDIR /app

# Salin file requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh project
COPY . .

# Jalankan aplikasi Flask
CMD ["python", "main.py"]
