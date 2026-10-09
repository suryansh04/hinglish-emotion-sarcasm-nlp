"""Second-opinion check of the local model's output using the Gemini API.

The key is read from the GEMINI_API_KEY environment variable. Uses only the
standard library, so no extra dependency is needed.
"""
import json
import os
import urllib.error
import urllib.request

from .model import CONFIG

URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

PROMPT = """You are an expert in Hinglish (romanised Hindi-English) text.
Text: "{text}"
A local model predicted: emotion={emotion}, sarcastic={sarcastic}.
Decide independently what the writer's true emotion is (one of joy, anger, sadness, fear)
and whether the text is sarcastic. Then say whether the local prediction is correct.
Reply with JSON only: {{"emotion": str, "sarcastic": bool, "agrees": bool, "reason": str}}"""


class GeminiError(RuntimeError):
    pass


def verify(text, result):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise GeminiError("GEMINI_API_KEY is not set")
    cfg = CONFIG["gemini"]
    prompt = PROMPT.format(text=text, emotion=result["emotion"], sarcastic=result["sarcastic"])
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0},
    }
    req = urllib.request.Request(
        URL.format(model=cfg["model"]), data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=cfg["timeout_seconds"]) as resp:
            payload = json.load(resp)
        return json.loads(payload["candidates"][0]["content"]["parts"][0]["text"])
    except urllib.error.HTTPError as e:
        raise GeminiError(f"Gemini API error {e.code}") from e
    except (urllib.error.URLError, KeyError, IndexError, ValueError) as e:
        raise GeminiError(f"Gemini request failed: {e}") from e
