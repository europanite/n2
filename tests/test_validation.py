from scripts.generate_sentence import is_valid_sentence, normalize_output


def test_normalize_output_merges_lines() -> None:
    raw = " 彼は困惑し、\n うんこを踏んだことに気づいて沈黙した。 \n"
    assert normalize_output(raw) == "彼は困惑し、 うんこを踏んだことに気づいて沈黙した。"


def test_is_valid_sentence_accepts_single_sentence() -> None:
    text = "彼は突然の腹痛に動揺し、うんこを我慢したまま面接に臨んだ。"
    assert is_valid_sentence(text) is True


def test_is_valid_sentence_rejects_missing_keyword() -> None:
    text = "彼は突然の腹痛に動揺し、そのまま面接に臨んだ。"
    assert is_valid_sentence(text) is False


def test_is_valid_sentence_rejects_multiple_sentences() -> None:
    text = "彼は困惑した。うんこを踏んだからだ。"
    assert is_valid_sentence(text) is False


def test_is_valid_sentence_rejects_explanatory_prefix() -> None:
    text = "例文：彼はうんこを見て困惑した。"
    assert is_valid_sentence(text) is False
