"""Sanity checks on the canonical vocabulary table. These pass today."""

from synergyscript.keywords import (
    PHRASES_LONGEST_FIRST,
    PHRASE_TOKENS,
    RESERVED_WORDS,
)


def test_phrases_sorted_longest_first():
    word_counts = [len(phrase.split()) for phrase, _ in PHRASES_LONGEST_FIRST]
    assert word_counts == sorted(word_counts, reverse=True)


def test_more_specific_phrase_precedes_prefix():
    # "pivot to" (ELIF) must be tried before "pivot" (ELSE).
    phrases = [phrase for phrase, _ in PHRASES_LONGEST_FIRST]
    assert phrases.index("pivot to") < phrases.index("pivot")


def test_reserved_words_include_phrase_words():
    assert {"circle", "back", "drill", "flagpole"} <= RESERVED_WORDS


def test_value_literals_reserved():
    for word in ("aligned", "blocked", "tbd"):
        assert word in PHRASE_TOKENS
