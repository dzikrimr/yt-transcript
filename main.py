from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

ASSEMBLYAI_API_KEY = "1473e55c39fb4757a910e568f91ec0c2"

ASSEMBLYAI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"


@app.route("/")
def index():
    return "🎧 YouTube Transcript API is running!"


@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "Parameter 'url' diperlukan"}), 400

    try:
        # 1️⃣ Kirim video YouTube ke AssemblyAI
        transcript_request = requests.post(
            ASSEMBLYAI_TRANSCRIPT_URL,
            headers={"authorization": ASSEMBLYAI_API_KEY},
            json={"audio_url": video_url, "language_detection": True},
        )

        transcript_id = transcript_request.json().get("id")
        if not transcript_id:
            return jsonify({"error": "Gagal memulai transkripsi"}), 500

        # 2️⃣ Tunggu proses selesai
        while True:
            poll = requests.get(
                f"{ASSEMBLYAI_TRANSCRIPT_URL}/{transcript_id}",
                headers={"authorization": ASSEMBLYAI_API_KEY},
            )
            status = poll.json()["status"]

            if status == "completed":
                text = poll.json()["text"]
                return jsonify({
                    "status": "success",
                    "transcript": text
                })

            elif status == "error":
                return jsonify({"error": poll.json().get("error", "Gagal transkripsi")}), 500

            time.sleep(5)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
