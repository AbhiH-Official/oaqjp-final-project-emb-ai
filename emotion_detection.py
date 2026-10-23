import requests


def emotion_detector(text_to_analyze):
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id":
            "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=input_json,
            timeout=30
        )

        # Handle blank input or other bad requests
        if response.status_code == 400:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        response.raise_for_status()
        result = response.json()

        emotions = result["emotionPredictions"][0]["emotion"]

        scores = {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"]
        }

        scores["dominant_emotion"] = max(
            scores, key=scores.get
        )

        return scores

    except requests.RequestException:
        raise
    except (KeyError, IndexError, TypeError, ValueError):
        raise ValueError("Unexpected response from emotion API")