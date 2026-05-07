import pytest
from word_counter import count_words, analyze, WordStats

def test_count_words_basic():
    result = count_words("hello world hello")
    assert result == {"hello": 2, "world": 1}

def test_count_words_case_insensitive():
    result = count_words("hello Hello hello")
    assert result == {"hello": 3}