from app.util import csv


def test_detect_separator_comma():
    content = "a,b,c\n1,2,3"
    assert csv.detect_separator(content) == ","


def test_detect_separator_tab():
    content = "a\tb\tc\n1\t2\t3"
    assert csv.detect_separator(content) == "\t"


def test_detect_separator_semicolon():
    content = "a;b;c\n1;2;3"
    assert csv.detect_separator(content) == ";"


def test_detect_separator_none():
    content = "abc\ndef"
    assert csv.detect_separator(content) == ";"


def test_detect_separator_mixed():
    content = "a,b,c\n1;2;3\n4,5,6"
    assert csv.detect_separator(content) == ","
