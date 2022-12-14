from ga4gh_json_canonical.functions import (dict_to_sorted_by_utf16_tuple,
                                            float_to_int_if_whole_and_not_large_exp,
                                            int_to_str_if_too_large,
                                            to_utf16_tuple)
from ga4gh_json_canonical.util import JSON, JsonDataPreprocessor


def test_float_to_int_if_whole_and_not_large_exp():
    assert float_to_int_if_whole_and_not_large_exp(1.0) == 1
    assert type(float_to_int_if_whole_and_not_large_exp(1.0)) is int

    assert float_to_int_if_whole_and_not_large_exp(-1.0) == -1
    assert type(float_to_int_if_whole_and_not_large_exp(-1.0)) is int

    assert float_to_int_if_whole_and_not_large_exp(1.5) == 1.5
    assert type(float_to_int_if_whole_and_not_large_exp(1.5)) is float

    assert float_to_int_if_whole_and_not_large_exp(-1.5) == -1.5
    assert type(float_to_int_if_whole_and_not_large_exp(-1.5)) is float

    assert float_to_int_if_whole_and_not_large_exp(1e10) == 10000000000
    assert type(float_to_int_if_whole_and_not_large_exp(1e10)) is int

    assert float_to_int_if_whole_and_not_large_exp(1e20) == 100000000000000000000
    assert type(float_to_int_if_whole_and_not_large_exp(1e20)) is int

    assert float_to_int_if_whole_and_not_large_exp(1e21) == 1e21
    assert type(float_to_int_if_whole_and_not_large_exp(1e21)) is float

    assert float_to_int_if_whole_and_not_large_exp(-1e20) == -100000000000000000000
    assert type(float_to_int_if_whole_and_not_large_exp(-1e20)) is int

    assert float_to_int_if_whole_and_not_large_exp(-1e21) == -1e21
    assert type(float_to_int_if_whole_and_not_large_exp(-1e21)) is float

    assert float_to_int_if_whole_and_not_large_exp(1e-1) == 0.1
    assert type(float_to_int_if_whole_and_not_large_exp(1e-1)) is float

    assert float_to_int_if_whole_and_not_large_exp(-1e-1) == -0.1
    assert type(float_to_int_if_whole_and_not_large_exp(-1e-1)) is float


def test_int_to_str_if_too_large():
    assert int_to_str_if_too_large(9223372036854775807) == 9223372036854775807
    assert type(int_to_str_if_too_large(9223372036854775807)) is int

    assert int_to_str_if_too_large(-9223372036854775807) == -9223372036854775807
    assert type(int_to_str_if_too_large(-9223372036854775807)) is int

    assert int_to_str_if_too_large(-9223372036854775808) == '-9223372036854775808'
    assert type(int_to_str_if_too_large(-9223372036854775808)) is str

    assert int_to_str_if_too_large(-9223372036854775808) == '-9223372036854775808'
    assert type(int_to_str_if_too_large(-9223372036854775808)) is str


def test_to_utf16_tuple():
    assert to_utf16_tuple('???') == (8364,)
    assert to_utf16_tuple('1') == (49,)
    assert to_utf16_tuple('\r') == (13,)
    assert to_utf16_tuple('???') == (64307,)
    assert to_utf16_tuple('????') == (55357, 56832)
    assert to_utf16_tuple('\x80') == (128,)
    assert to_utf16_tuple('??') == (246,)
    assert to_utf16_tuple('???1\r???????\x80??') == (8364, 49, 13, 64307, 55357, 56832, 128, 246)


def test_dict_to_sorted_by_utf16_tuple():
    assert dict_to_sorted_by_utf16_tuple({'b': 2, 'a': 1}) == {'a': 1, 'b': 2}
    assert dict_to_sorted_by_utf16_tuple({'???????': 2, '???????': 1}) == {'???????': 1, '???????': 2}


def test_dict_to_sorted_by_utf16_tuple_recursive():
    def dict_to_sorted_by_utf16_tuple_recursive(data: JSON):
        _dict_to_sorted_by_utf16_tuple_recursive = JsonDataPreprocessor(
            dict_func=dict_to_sorted_by_utf16_tuple)
        return _dict_to_sorted_by_utf16_tuple_recursive(data)

    assert dict_to_sorted_by_utf16_tuple_recursive({
        'b': {
            'd': 3, 'c': 2
        }, 'a': 1
    }) == {
        'b': {
            'c': 2, 'd': 3
        }, 'a': 1
    }
    assert dict_to_sorted_by_utf16_tuple_recursive({
        'a': [{
            '???????': 3, '???????': 2
        }, 4], 'b': 2
    }) == {
        'a': [{
            '???????': 2, '???????': 3
        }, 4], 'b': 2
    }
