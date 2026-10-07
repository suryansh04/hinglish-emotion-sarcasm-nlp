"""Stratified 5-fold cross-validation for both tasks."""
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import StratifiedKFold

from .model import CONFIG, HinglishAnalyzer, load_corpus


def run(folds=CONFIG["cv_folds"], seed=CONFIG["random_seed"]):
    texts, emo, sarc = map(np.array, load_corpus())
    # stratify on emotion+sarcasm jointly so every fold sees every combination
    strata = np.array([f"{e}{s}" for e, s in zip(emo, sarc)])
    pe, ps = np.empty(len(texts), dtype=object), np.zeros(len(texts), int)
    for tr, te in StratifiedKFold(folds, shuffle=True, random_state=seed).split(texts, strata):
        m = HinglishAnalyzer().fit(texts[tr], emo[tr], sarc[tr].tolist())
        for i in te:
            r = m.predict(texts[i])
            pe[i], ps[i] = r["emotion"], int(r["sarcastic"])
    print(f"Emotion  accuracy: {accuracy_score(emo, pe):.3f}  macro-F1: {f1_score(emo, pe, average='macro'):.3f}")
    print(classification_report(emo, pe, zero_division=0))
    print(f"Sarcasm  accuracy: {accuracy_score(sarc.astype(int), ps):.3f}  F1: {f1_score(sarc.astype(int), ps):.3f}")

