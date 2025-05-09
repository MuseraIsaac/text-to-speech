from flask import Flask, request, send_file, jsonify
import os
import uuid
from TTS.api import TTS

app = Flask(__name__)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route("/text2speech/api/tts", methods=["POST"])
def synthesize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]
    output_path = f"/tmp/{uuid.uuid4().hex}.wav"
    tts.tts_to_file(text=text, file_path=output_path)

    return send_file(output_path, as_attachment=True, mimetype="audio/wav")

if __name__ == "__main__":
    # Run the app on port 5001
    app.run(host="127.0.0.1", port=5001)
