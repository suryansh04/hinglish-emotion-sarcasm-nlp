"""Interactive terminal interface: type Hinglish text, get emotion + sarcasm."""
import argparse

from .model import HinglishAnalyzer, load_corpus


def build():
    return HinglishAnalyzer().fit(*load_corpus())


def show(r):
    print(f"  normalised : {r['normalized']}")
    for e, p in sorted(r["emotion_probs"].items(), key=lambda kv: -kv[1]):
        print(f"  {e:<8} {'#' * int(p * 30):<30} {p:5.1%}")
    tag = "SARCASTIC" if r["sarcastic"] else "sincere"
    print(f"  => emotion: {r['emotion'].upper()} | tone: {tag} (sarcasm score {r['sarcasm_prob']:.2f})")
    if r["sarcastic"]:
        print("  note: surface wording may be positive, but the intended emotion is the negative one.")


def main():
    ap = argparse.ArgumentParser(description="Hinglish emotion & sarcasm analyser")
    ap.add_argument("text", nargs="*", help="analyse this text once and exit")
    ap.add_argument("--evaluate", action="store_true", help="run cross-validation and exit")
    args = ap.parse_args()
    if args.evaluate:
        from .evaluate import run
        return run()
    analyzer = build()
    if args.text:
        return show(analyzer.predict(" ".join(args.text)))
    print("Hinglish Emotion & Sarcasm Analyzer  (type 'quit' to exit)")
    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in {"quit", "exit", "q"}:
            break
        if text:
            show(analyzer.predict(text))


if __name__ == "__main__":
    main()
