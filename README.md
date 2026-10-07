# Hinglish Emotion & Sarcasm Analyzer

A terminal NLP tool that reads romanised Hindi-English ("Hinglish") text and
predicts **what emotion the writer feels** and **whether they are being sarcastic**.

> "waah bahut accha, ghanta bhar late aaye ho" → *surface: praise, actual: **anger** (sarcastic)*

## Why this problem is hard
- **Code-mixing** – Hindi and English words share one sentence.
- **No standard spelling** – *accha / acha / achha* are all valid.
- **Sarcasm flips polarity** – positive words describe a negative situation, so
  plain sentiment classifiers get it wrong.

## Approach
1. **Normaliser** (`normalize.py`) – lowercases, tags emojis, shrinks elongations
   (*waaaah → waah*) and maps spelling variants to canonical forms.
2. **Emotion classifier** – char n-gram (2–4) + word n-gram TF-IDF into logistic
   regression; char n-grams handle spelling noise.
3. **Transliteration-aware lexicon** (`lexicon.py`) – emotion word lists blended
   with the classifier (70 / 30) for robustness on unseen words.
4. **Sarcasm detector** – TF-IDF features plus hand-built cues: positive surface
   words, negative-situation words, their *contrast*, and irony markers
   (*"kya baat hai"*, 🙄).

Emotions: `joy`, `anger`, `sadness`, `fear`.

## Setup & usage
```bash
pip install -r requirements.txt

python -m hinglish_nlp                       # interactive mode
python -m hinglish_nlp "mujhe bahut dar lag raha hai"   # one-shot
python -m hinglish_nlp --evaluate            # 5-fold cross-validation
python -m pytest tests                       # unit tests
```

Example session:
```
> wah kya kismat hai mera hi number ke din network gaya
  anger / sadness probabilities …
  => emotion: SADNESS | tone: SARCASTIC
```

## Results (5-fold stratified CV, 68 hand-written sentences)
| Task    | Accuracy | F1 |
|---------|----------|----|
| Emotion | 0.735    | 0.734 (macro) |
| Sarcasm | 0.912    | 0.880 |

## Limitations & future work
- The corpus is small and hand-written, so scores are indicative, not a benchmark.
  Next step: train on a larger corpus such as the public Hinglish datasets from SemEval/LinCE.
- Romanised text only (no Devanagari).
- Could be extended with multilingual transformer embeddings (e.g. MuRIL, XLM-R).

## Structure
```
hinglish_nlp/  normalize.py  lexicon.py  model.py  evaluate.py  cli.py
data/          hinglish_corpus.csv
config.json    model and evaluation settings
PROMPT.md      problem statement and requirements
tests/
```

