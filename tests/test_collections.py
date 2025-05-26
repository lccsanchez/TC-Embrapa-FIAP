from app.util import collections


def test_filter_basic():
    data = [1, 2, 3, 4]
    result = collections.filter_collection(data, lambda x: x % 2 == 0)
    assert result == [2, 4]


def test_filter_empty():
    data = []
    result = collections.filter_collection(data, lambda x: True)
    assert result == []


def test_filter_exception():
    data = [1, 2, 3]

    def bad_predicate(x):
        raise ValueError("fail")

    result = collections.filter_collection(data, bad_predicate)
    assert result == []


def test_filter_all_false():
    data = [1, 2, 3]
    result = collections.filter_collection(data, lambda x: False)
    assert result == []
