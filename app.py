from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import numpy as np
import cv2
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict_emotion", methods=["POST"])
def predict_emotion():
    data = request.get_json()

    # Extract base64 image string
    img_data = data.get("image")
    if not img_data:
        return jsonify({"error": "No image data provided"}), 400

    # Remove the base64 header if present
    if "," in img_data:
        img_data = img_data.split(",")[1]

    # Decode base64 to bytes
    img_bytes = base64.b64decode(img_data)

    # Convert bytes to numpy array
    np_arr = np.frombuffer(img_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # DeepFace expects RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Run emotion analysis (enforce_detection=False to prevent errors)
    try:
        result = DeepFace.analyze(img_rgb, actions=["emotion"], enforce_detection=False)
        emotion = result[0]["dominant_emotion"]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"emotion": emotion})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
