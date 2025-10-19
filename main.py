from flask import Flask, request, jsonify
import yt_dlp
import whisper
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Whisper Transcript API is running!"

@app.route("/get_transcript")
def get_transcript():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Parameter 'id' diperlukan."}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    audio_path = "audio.mp3"

    try:
        # --- 1️⃣ Download audio ---
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # --- 2️⃣ Transcribe pakai Whisper ---
        model = whisper.load_model("base")  # bisa 'tiny', 'base', 'small', 'medium', 'large'
        result = model.transcribe(audio_path, language="id")

        # --- 3️⃣ Hapus file audio setelah selesai ---
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return jsonify({"transcript": result["text"]})

    except Exception as e:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
