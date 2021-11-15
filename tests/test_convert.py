from math import isclose

import pytest

from genetic.convert import int2bits, bits2int, float2bits, bits2float


@pytest.mark.parametrize('ivalue,low,expected', [
    [1, 0, '01'],
    [2, 0, '10' ],
    [3, 0, '11'],
    [2, 0, '00010' ],
    [1, 0, '001'],
    [1, 1, '00'],
    [3, 1, '10'],
    [3, -1, '100'],
    [2, -1, '00011' ],
])
def test_int2bits_success(ivalue, low, expected):
    assert int2bits(ivalue, low, len(expected)) == expected


@pytest.mark.parametrize('n_bits', [-1, 0 , -2])
def test_int2bits_not_validate_negative_n_bits(n_bits):
    with pytest.raises(ValueError):
        int2bits(1, 1, n_bits)


@pytest.mark.parametrize('bits,low,expected', [
    ['1', 0, 1],
    ['1', 1, 2],
    ['00001', 0, 1],
    ['00001', 3, 4],
    ['01', 0, 1],
    ['11', 0, 3],
    ['0011', 0, 3],
    ['101', 0, 5]
])
def test_bits2int_success(bits, low, expected):
    assert bits2int(bits, low) == expected


@pytest.mark.skip
@pytest.mark.parametrize('fvalue,low,high,n_bits,expected', [
    [10, 10, 11, 16, '0000000000000000'],
    [10, 10, 11, 2, '00'],
    [11, 10, 12, 2, '10'],
    [10.5, 10, 12, 2, '01'],
])
def test_float2bits(fvalue, low, high, n_bits, expected):
    assert float2bits(fvalue=fvalue, low=low, high=high, n_bits=n_bits) == expected


@pytest.mark.parametrize('bits,low,high,expected', [
    ['0000000000000000', 10, 11, 10],
    ['00', 10, 11, 10],
    ['10', 10, 12, 11],
    ['01', 10, 12, 10.5],
])
def test_bits2float(bits, low, high, expected):
    assert isclose(bits2float(bits, low, high), expected)
