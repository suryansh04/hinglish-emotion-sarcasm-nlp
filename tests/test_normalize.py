from hinglish_nlp.normalize import normalize


def test_spelling_variants_collapse():
    assert normalize("accha achha") == "acha acha"


def test_elongation_and_emoji():
    assert normalize("waaaah ??") == "waah emo_laugh"
