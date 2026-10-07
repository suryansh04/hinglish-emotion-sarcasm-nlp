# Project Prompt

## Problem statement
Build a command-line NLP system for **Hinglish** (romanised Hindi-English
code-mixed text) that, for any sentence typed by the user, reports:

1. the underlying **emotion** (joy, anger, sadness, fear), and
2. whether the writer is being **sarcastic**.

## Requirements
- Runs fully locally; input is read from the terminal and results are printed there.
- Handle non-standard spellings (accha / acha / achha), elongations (waaah) and emojis.
- Combine a statistical classifier with a hand-built emotion lexicon.
- Treat sarcasm as a contrast between positive wording and a negative situation.
- All tunable values live in `config.json`.
- Provide an evaluation mode (stratified k-fold cross-validation) with accuracy and F1.
- Include unit tests and a README explaining approach, usage and limitations.

## Expected behaviour
Input:  `waah bahut accha, ghanta bhar late aaye ho`
Output: emotion **anger**, tone **sarcastic**
