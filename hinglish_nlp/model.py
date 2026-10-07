"""Emotion + sarcasm model for Hinglish text."""
import csv
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from .lexicon import EMOTION_LEXICON, IRONY_MARKERS, NEGATIVE_SITUATION, POSITIVE_SURFACE
from .normalize import normalize

DATA = Path(__file__).resolve().parent.parent / "data" / "hinglish_corpus.csv"
EMOTIONS = list(EMOTION_LEXICON)
LEXICON_WEIGHT = 0.3  # share of the lexicon score in the final emotion blend


def load_corpus(path=DATA):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r["text"] for r in rows], [r["emotion"] for r in rows], [int(r["sarcastic"]) for r in rows]


def lexicon_scores(norm_text):
    toks = norm_text.split()
    raw = np.array([sum(t in words for t in toks) for words in EMOTION_LEXICON.values()], float)
    return raw / raw.sum() if raw.sum() else np.full(len(EMOTIONS), 1 / len(EMOTIONS))


def sarcasm_features(norm_text):
    """Hand-built cues: positive wording + negative situation + irony markers."""
    toks = set(norm_text.split())
    pos = len(toks & POSITIVE_SURFACE)
    neg = len(toks & NEGATIVE_SITUATION)
    irony = sum(m in norm_text for m in IRONY_MARKERS)
    contrast = float(pos > 0 and neg > 0)
    return [pos, neg, irony, contrast, contrast * (pos + neg), float("emo_laugh" in toks)]


class HinglishAnalyzer:
    def __init__(self):
        self.vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), sublinear_tf=True)
        self.word_vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.emotion_clf = LogisticRegression(C=10, max_iter=1000)
        self.sarcasm_clf = LogisticRegression(C=5, max_iter=1000, class_weight="balanced")

    def _text_matrix(self, norm, fit=False):
        if fit:
            return hstack([self.vec.fit_transform(norm), self.word_vec.fit_transform(norm)]).tocsr()
        return hstack([self.vec.transform(norm), self.word_vec.transform(norm)]).tocsr()

    def _sarcasm_matrix(self, X, norm):
        return hstack([X, csr_matrix([sarcasm_features(t) for t in norm])]).tocsr()

    def fit(self, texts, emotions, sarcasm):
        norm = [normalize(t) for t in texts]
        X = self._text_matrix(norm, fit=True)
        self.emotion_clf.fit(X, emotions)
        self.sarcasm_clf.fit(self._sarcasm_matrix(X, norm), sarcasm)
        return self

    def predict(self, text):
        norm = normalize(text)
        X = self._text_matrix([norm])
        clf_p = dict(zip(self.emotion_clf.classes_, self.emotion_clf.predict_proba(X)[0]))
        lex_p = dict(zip(EMOTIONS, lexicon_scores(norm)))
        probs = {e: (1 - LEXICON_WEIGHT) * clf_p.get(e, 0) + LEXICON_WEIGHT * lex_p[e] for e in EMOTIONS}
        sarc = float(self.sarcasm_clf.predict_proba(self._sarcasm_matrix(X, [norm]))[0][1])
        emotion = max(probs, key=probs.get)
        return {"normalized": norm, "emotion": emotion, "emotion_probs": probs,
                "sarcasm_prob": sarc, "sarcastic": sarc >= 0.5}
