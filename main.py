import os
from flask import Flask, request, jsonify
import yt_dlp
import whisper

app = Flask(__name__)

# Muat model Whisper. Model "base" adalah kompromi yang baik antara kecepatan dan akurasi.
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded.")

@app.route("/")
def index():
    return "yt-dlp + Whisper API is running!"

@app.route("/get_transcript")
def get_transcript():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Parameter 'id' video YouTube diperlukan."}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    # Path untuk menyimpan file audio sementara
    audio_path = f"/tmp/{video_id}.m4a"

    try:
        # Konfigurasi yt-dlp untuk download audio terbaik dengan format m4a
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'outtmpl': audio_path,
            'quiet': True,
        }

        # Download audio menggunakan yt-dlp
        print(f"Downloading audio for {video_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Audio downloaded.")

        # Transkripsi audio menggunakan Whisper
        print(f"Transcribing audio for {video_id}...")
        result = model.transcribe(audio_path, fp16=False) # fp16=False untuk kompatibilitas CPU
        full_text = result["text"]
        print("Transcription complete.")

        return jsonify({"transcript": full_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500 # Gunakan 500 untuk Internal Server Error
    finally:
        # Selalu hapus file audio sementara setelah selesai, baik berhasil maupun gagal
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Cleaned up temporary file: {audio_path}")

if __name__ == "__main__":
    app.run(debug=True)