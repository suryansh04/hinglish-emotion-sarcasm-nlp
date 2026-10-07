"""Text normalisation for romanised Hindi-English (Hinglish) text.

Hinglish has no standard spelling: "accha", "acha" and "achha" are the same
word. We collapse such variants to one canonical form so the downstream
models see fewer, denser features.
"""
import re

# canonical form -> spelling variants seen in social-media text
VARIANTS = {
    "acha": ["accha", "achha", "acchha", "achcha"],
    "nahi": ["nahin", "nai", "nahii", "nhi", "nai"],
    "bahut": ["bohot", "bahot", "bhot", "boht", "bohut"],
    "kya": ["kia", "kyaa"],
    "hai": ["hain", "he", "h"],
    "mujhe": ["mujhko", "muje"],
    "bakwas": ["bakwaas", "bakwass", "bkwas"],
    "yaar": ["yar", "yaaar", "yar"],
    "mast": ["mast", "mastt"],
    "dukh": ["dukhi", "dukhh"],
    "gussa": ["gusa", "gussaa"],
    "khush": ["khus", "khushh"],
    "pyaar": ["pyar", "pyaaar"],
    "waah": ["wah", "waa", "wahh", "vah", "waaah"],
    "bilkul": ["bilkull", "bilkool"],
    "zabardast": ["jabardast", "zabardasth", "jabrdast"],
    "kamaal": ["kamal", "kamaaal"],
}
CANONICAL = {v: k for k, vs in VARIANTS.items() for v in vs}

EMOJI_TAGS = {
    "😂": " emo_laugh ", "🤣": " emo_laugh ", "😅": " emo_laugh ",
    "😊": " emo_happy ", "😍": " emo_happy ", "❤": " emo_happy ", "🥳": " emo_happy ",
    "😡": " emo_angry ", "🤬": " emo_angry ", "😠": " emo_angry ",
    "😢": " emo_sad ", "😭": " emo_sad ", "💔": " emo_sad ",
    "😱": " emo_fear ", "😨": " emo_fear ", "😰": " emo_fear ",
    "🙄": " emo_eyeroll ", "😒": " emo_eyeroll ", "🙃": " emo_eyeroll ",
}

_ELONG = re.compile(r"(.)\1{2,}")
_TOKEN = re.compile(r"[a-z0-9_']+|[!?]+")


def normalize(text: str) -> str:
    """Lowercase, tag emojis, shrink elongations, canonicalise spellings."""
    text = text.lower()
    for emo, tag in EMOJI_TAGS.items():
        text = text.replace(emo, tag)
    text = _ELONG.sub(r"\1\1", text)  # soooo -> soo
    tokens = _TOKEN.findall(text)
    return " ".join(CANONICAL.get(t, t) for t in tokens)
