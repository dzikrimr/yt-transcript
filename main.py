import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route("/")
def index():
    # Rute dasar untuk mengecek apakah server berjalan
    return "Transcript API is running!"

@app.route("/get_transcript")
def get_transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Parameter 'id' video YouTube diperlukan."}), 400

    try:
        # Mencoba mengambil transkrip dalam bahasa Indonesia, jika gagal coba Inggris
        # Ini akan otomatis mencari transkrip yang dibuat manual ATAU yang dibuat otomatis oleh YouTube
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['id', 'en'])
        
        # Menggabungkan semua teks menjadi satu string panjang, dipisahkan spasi
        full_text = " ".join([item['text'] for item in transcript_list])
        
        return jsonify({"transcript": full_text})

    except TranscriptsDisabled:
        # Error spesifik jika pemilik video menonaktifkan fitur transkrip
        return jsonify({"error": f"Transkrip dinonaktifkan untuk video ID: {video_id}"}), 404
    
    except NoTranscriptFound:
        # Error spesifik jika tidak ada transkrip dalam bahasa yang dicari (id atau en)
        return jsonify({"error": f"Tidak ditemukan transkrip dalam bahasa Indonesia atau Inggris untuk video ID: {video_id}"}), 404

    except Exception as e:
        # Error umum untuk semua masalah lain (misal: video tidak ada, video pribadi, dll)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Baris ini hanya untuk testing di komputer lokal, tidak digunakan oleh Gunicorn di Railway
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))