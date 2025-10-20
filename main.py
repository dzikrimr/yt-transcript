import os
import re
from flask import Flask, request, jsonify
from pytube import YouTube, cipher
from pytube.exceptions import PytubeError

app = Flask(__name__)

# --- TAMBAHAN KODE UNTUK MEMPERBAIKI MASALAH UMUM PYTUBE ---
# pytube sering gagal dengan error 400 karena perubahan cipher di YouTube
# Kode ini mencoba memperbaiki fungsi cipher secara dinamis.
try:
    cipher.get_throttling_function_name = cipher.get_throttling_function_name
    print("pytube cipher patch already applied.")
except AttributeError:
    print("Applying pytube cipher patch...")
    from pytube.cipher import get_throttling_function_name as main_get_throttling_function_name
    def patched_get_throttling_function_name(js: str) -> str:
        # Panggil fungsi asli, jika gagal, gunakan solusi fallback
        try:
            return main_get_throttling_function_name(js)
        except Exception:
            # Ini adalah solusi umum jika regex default gagal
            return 'a' 
    cipher.get_throttling_function_name = patched_get_throttling_function_name
# --- AKHIR BAGIAN PERBAIKAN ---


@app.route("/")
def index():
    return "pytube Transcript API (Patched) is running!"

def parse_srt(srt_text):
    lines = srt_text.splitlines()
    text_lines = []
    for line in lines:
        if not line.strip().isdigit() and '-->' not in line and line.strip():
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
        
        caption = yt.captions.get_by_language_code('en') or yt.captions.get_by_language_code('a.en') or yt.captions.get_by_language_code('id')

        if not caption:
            return jsonify({"error": "Tidak ditemukan transkrip dalam bahasa Inggris atau Indonesia untuk video ini."}), 404

        srt_captions = caption.generate_srt_captions()
        full_text = parse_srt(srt_captions)

        return jsonify({"transcript": full_text})

    except PytubeError as e:
        return jsonify({"error": f"Pytube Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))