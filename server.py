
"""Flask server for the emotion detection application."""

import requests
from flask import Flask, jsonify, request

from emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/emotionDetector", methods=["POST"])
def detect_emotion():
    """Analyze the supplied text and return its detected emotions."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "textToAnalyze" not in data:
        return jsonify({"error": "Please provide textToAnalyze."}), 400

    text_to_analyze = data["textToAnalyze"]

    if not isinstance(text_to_analyze, str):
        return jsonify({"error": "textToAnalyze must be a string."}), 400

    try:
        result = emotion_detector(text_to_analyze)

        if result["dominant_emotion"] is None:
            return "Invalid text! Please try again!", 200

        return jsonify(result), 200

    except requests.RequestException:
        app.logger.exception("Emotion API request failed")
        return jsonify({
            "error": "Unable to contact the emotion detection service."
        }), 502

    except (KeyError, TypeError, ValueError):
        app.logger.exception("Emotion detection failed")
        return jsonify({"error": "Emotion detection failed."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
