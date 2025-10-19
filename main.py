from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

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
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['id', 'en'])
        # Menggabungkan semua teks menjadi satu string panjang
        full_text = " ".join([item['text'] for item in transcript_list])
        return jsonify({"transcript": full_text})
    except Exception as e:
        # Memberikan pesan error jika transkrip tidak ditemukan atau terjadi kesalahan lain
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True)