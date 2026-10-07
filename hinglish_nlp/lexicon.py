"""Small emotion lexicon over normalised Hinglish tokens, plus the word
lists used to detect the positive-surface / negative-situation contrast that
characterises sarcasm."""

EMOTION_LEXICON = {
    "joy": {"khush", "maza", "mast", "pyaar", "pyara", "sundar", "jeet", "jeetna", "celebrate",
            "masti", "proud", "zabardast", "kamaal", "yay", "emo_happy", "fresh", "happy", "love"},
    "anger": {"gussa", "bakwas", "bardasht", "irritate", "dhokha", "jhooth", "pagal", "bura",
              "kharab", "bhaad", "emo_angry", "hate", "idiot", "waste", "maaf"},
    "sadness": {"dukh", "rona", "udaasi", "akela", "miss", "aansu", "nirash", "toot", "yaad",
                "emo_sad", "fail", "sad", "cry"},
    "fear": {"dar", "darr", "ghabrahat", "kaanp", "kaanpna", "tension", "pasine", "pressure",
             "emo_fear", "scared", "afraid", "andhere"},
}

# words that sound positive on the surface
POSITIVE_SURFACE = {"waah", "kamaal", "zabardast", "mast", "acha", "great", "nice", "shukriya",
                    "maza", "majaa", "khushi", "bohot", "bahut", "imaandar", "bilkul", "sahi"}

# words describing a negative situation
NEGATIVE_SITUATION = {"late", "nahi", "fail", "gir", "gira", "kharab", "bhula", "bhul", "rejected",
                      "daant", "taane", "beizzati", "waste", "ghanta", "jhooth", "hasna", "bijli",
                      "network", "dhokha", "akele", "tod", "toota", "padega", "parcel", "credit",
                      "kabhi", "mat", "bhi"}

IRONY_MARKERS = {"emo_eyeroll", "haan haan", "oh great", "oh nice", "wah beta", "waah bhai",
                 "bilkul sahi", "kya baat hai", "kya mast", "kya kamaal", "kya timing"}
