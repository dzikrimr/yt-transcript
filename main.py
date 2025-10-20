import os
import re
from flask import Flask, request, jsonify
from pytube import YouTube
from pytube.exceptions import PytubeError

app = Flask(__name__)

@app.route("/")
def index():
    # Rute dasar untuk mengecek apakah server berjalan
    return "pytube Transcript API is running!"

def parse_srt(srt_text):
    """Fungsi sederhana untuk membersihkan teks SRT menjadi kalimat biasa."""
    lines = srt_text.splitlines()
    text_lines = []
    for line in lines:
        # Abaikan baris yang berisi angka (nomor urut) atau timestamp (-->)
        if not line.strip().isdigit() and '-->' not in line and line.strip():
            # Hapus tag HTML seperti <i...> (untuk teks miring)
            clean_line = re.sub(r'<.*?>', '', line)
            text_lines.append(clean_line.strip())
    return " ".join(text_lines)

@app.route("/get_transcript")
def get_transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Parameter 'id' video YouTube diperlukan."}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        yt = YouTube(video_url)
        
        # Cari transkrip: prioritas manual bahasa Inggris, lalu otomatis Inggris, lalu manual Indonesia
        caption = yt.captions.get_by_language_code('en') or yt.captions.get_by_language_code('a.en') or yt.captions.get_by_language_code('id')

        if not caption:
            return jsonify({"error": "Tidak ditemukan transkrip dalam bahasa Inggris atau Indonesia untuk video ini."}), 404

        # Dapatkan transkrip dalam format SRT dan bersihkan
        srt_captions = caption.generate_srt_captions()
        full_text = parse_srt(srt_captions)

        return jsonify({"transcript": full_text})

    except PytubeError as e:
        # Tangani error spesifik dari pytube (misal: video tidak ada, dibatasi usia, dll)
        return jsonify({"error": f"Pytube Error: {str(e)}"}), 500
    except Exception as e:
        # Tangani semua error lainnya
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))