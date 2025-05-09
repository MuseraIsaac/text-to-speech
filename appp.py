from flask import Flask, request, send_file, jsonify
import os
import uuid
from TTS.api import TTS

app = Flask(__name__)

# Speaker map (update with the actual paths to your models)
speaker_map = {
    "p225": "tts_models/en/vctk/vits",
    "p226": "tts_models/en/vctk/vits",
    "p227": "tts_models/en/vctk/vits",
    "p228": "tts_models/en/vctk/vits",
    "p229": "tts_models/en/vctk/vits",
    "p230": "tts_models/en/vctk/vits",
    "p231": "tts_models/en/vctk/vits",
    "p232": "tts_models/en/vctk/vits",
    "p233": "tts_models/en/vctk/vits",
    "p234": "tts_models/en/vctk/vits",
    "p236": "tts_models/en/vctk/vits",
    "p237": "tts_models/en/vctk/vits",
    "p238": "tts_models/en/vctk/vits",
    "p239": "tts_models/en/vctk/vits",
    "p240": "tts_models/en/vctk/vits",
    "p241": "tts_models/en/vctk/vits",
    "p243": "tts_models/en/vctk/vits",
    "p244": "tts_models/en/vctk/vits",
    "p245": "tts_models/en/vctk/vits",
    "p246": "tts_models/en/vctk/vits",
    "p247": "tts_models/en/vctk/vits",
    "p248": "tts_models/en/vctk/vits",
    "p249": "tts_models/en/vctk/vits",
    "p250": "tts_models/en/vctk/vits",
    "p251": "tts_models/en/vctk/vits",
    "p252": "tts_models/en/vctk/vits",
    "p253": "tts_models/en/vctk/vits",
    "p254": "tts_models/en/vctk/vits",
    "p255": "tts_models/en/vctk/vits",
    "p256": "tts_models/en/vctk/vits",
    "p257": "tts_models/en/vctk/vits",
    "p258": "tts_models/en/vctk/vits",
    "p259": "tts_models/en/vctk/vits",
    "p260": "tts_models/en/vctk/vits",
    "p261": "tts_models/en/vctk/vits",
    "p262": "tts_models/en/vctk/vits",
    "p263": "tts_models/en/vctk/vits",
    "p264": "tts_models/en/vctk/vits",
    "p265": "tts_models/en/vctk/vits",
    "p266": "tts_models/en/vctk/vits",
    "p267": "tts_models/en/vctk/vits",
    "p268": "tts_models/en/vctk/vits",
    "p269": "tts_models/en/vctk/vits",
    "p270": "tts_models/en/vctk/vits",
    "p271": "tts_models/en/vctk/vits",
    "p272": "tts_models/en/vctk/vits",
    "p273": "tts_models/en/vctk/vits",
    "p274": "tts_models/en/vctk/vits",
    "p275": "tts_models/en/vctk/vits",
    "p276": "tts_models/en/vctk/vits",
    "p277": "tts_models/en/vctk/vits",
    "p278": "tts_models/en/vctk/vits",
    "p279": "tts_models/en/vctk/vits",
    "p280": "tts_models/en/vctk/vits",
    "p281": "tts_models/en/vctk/vits",
    "p282": "tts_models/en/vctk/vits",
    "p283": "tts_models/en/vctk/vits",
    "p284": "tts_models/en/vctk/vits",
    "p285": "tts_models/en/vctk/vits",
    "p286": "tts_models/en/vctk/vits",
    "p287": "tts_models/en/vctk/vits",
    "p288": "tts_models/en/vctk/vits",
    "p292": "tts_models/en/vctk/vits",
    "p293": "tts_models/en/vctk/vits",
    "p294": "tts_models/en/vctk/vits",
    "p295": "tts_models/en/vctk/vits",
    "p297": "tts_models/en/vctk/vits",
    "p298": "tts_models/en/vctk/vits",
    "p299": "tts_models/en/vctk/vits",
    "p300": "tts_models/en/vctk/vits",
    "p301": "tts_models/en/vctk/vits",
    "p302": "tts_models/en/vctk/vits",
    "p303": "tts_models/en/vctk/vits",
    "p304": "tts_models/en/vctk/vits",
    "p305": "tts_models/en/vctk/vits",
    "p306": "tts_models/en/vctk/vits",
    "p307": "tts_models/en/vctk/vits",
    "p308": "tts_models/en/vctk/vits",
    "p310": "tts_models/en/vctk/vits",
    "p311": "tts_models/en/vctk/vits",
    "p312": "tts_models/en/vctk/vits",
    "p313": "tts_models/en/vctk/vits",
    "p314": "tts_models/en/vctk/vits",
    "p316": "tts_models/en/vctk/vits",
    "p317": "tts_models/en/vctk/vits",
    "p318": "tts_models/en/vctk/vits",
    "p323": "tts_models/en/vctk/vits",
    "p326": "tts_models/en/vctk/vits",
    "p329": "tts_models/en/vctk/vits",
    "p330": "tts_models/en/vctk/vits",
    "p333": "tts_models/en/vctk/vits",
    "p334": "tts_models/en/vctk/vits",
    "p335": "tts_models/en/vctk/vits",
    "p336": "tts_models/en/vctk/vits",
    "p339": "tts_models/en/vctk/vits",
    "p340": "tts_models/en/vctk/vits",
    "p341": "tts_models/en/vctk/vits",
    "p343": "tts_models/en/vctk/vits",
    "p345": "tts_models/en/vctk/vits",
    "p347": "tts_models/en/vctk/vits",
    "p351": "tts_models/en/vctk/vits",
    "p360": "tts_models/en/vctk/vits",
    "p361": "tts_models/en/vctk/vits",
    "p362": "tts_models/en/vctk/vits",
    "p363": "tts_models/en/vctk/vits",
    "p364": "tts_models/en/vctk/vits",
    "p374": "tts_models/en/vctk/vits",
    "p376": "tts_models/en/vctk/vits"
}

@app.route("/text2speech/api/tts", methods=["POST"])
def synthesize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]
    speaker = data.get("speaker", "ED")  # Default speaker if none provided
    
    # Find the model path for the selected speaker
    model_path = speaker_map.get(speaker)
    if not model_path:
        return jsonify({"error": "Invalid speaker"}), 400

    # Initialize TTS model with the selected speaker
    tts = TTS(model_name=model_path, progress_bar=False, gpu=False)
    
    # Generate speech to a file
    output_path = f"/tmp/{uuid.uuid4().hex}.wav"
    tts.tts_to_file(text=text, file_path=output_path)

    return send_file(output_path, as_attachment=True, mimetype="audio/wav")

if __name__ == "__main__":
    # Run the app on port 5001
    app.run(host="127.0.0.1", port=5001)
