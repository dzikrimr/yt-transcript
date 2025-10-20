from flask import Flask, request, jsonify
import subprocess
import os
import assemblyai as aai
import google.generativeai as genai

# 🔑 API Keys
ASSEMBLYAI_API_KEY = "1473e55c39fb4757a910e568f91ec0c2"
GEMINI_API_KEY = "AIzaSyDR45Ww-yQQqrCHgKYBLA8eXt5t6vBbmqw"

# Konfigurasi API
aai.settings.api_key = ASSEMBLYAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

@app.route("/")
def index():
    return "YouTube Summarizer API is running!"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    youtube_url = data.get("url")

    if not youtube_url:
        return jsonify({"error": "YouTube URL is required"}), 400

    try:
        # 1️⃣ Unduh audio dari YouTube pakai yt-dlp
        audio_path = "audio.mp3"
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", audio_path,
            "--max-filesize", "50M",  # batasi ukuran
            "--no-playlist",
            "--quiet",
            youtube_url
        ], check=True)

        # 2️⃣ Upload ke AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)

        if transcript.status != "completed":
            return jsonify({"error": "Transcription failed"}), 500

        text = transcript.text

        # 3️⃣ Kirim ke Gemini buat diringkas
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Please summarize this YouTube video transcript:\n\n{text}"

        response = model.generate_content(prompt)
        summary = response.text

        # 4️⃣ Hapus file audio setelah selesai
        os.remove(audio_path)

        return jsonify({
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
