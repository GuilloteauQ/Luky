#!/usr/bin/env python3

from tests import Test
from random import randint

#[test]
def test1():
    assert 2 > 3

#[test]
def test_sum_int():
    n = 100000
    somme = 0
    for i in range(1, n + 1):
        somme += i
    assert somme == (n + 1) * n / 2
#[test]
def test_sort():
    n = 1000000
    tab = [randint(0, n) for _ in range(n)]
    tab.sort()
    for i in range(n - 1):
        assert tab[i] <= tab[i + 1]
    assert tab[n - 2] <= tab[n - 1]
#[test]
def test_fibo():
    n = 140
    f1 = 1
    f2 = 1
    for _ in range(n - 2):
        f1, f2 = f2, f1 + f2
    assert f2 == 81055900096023504197206408605

# Test(test1, "Test1")
# Test(test_sum_int, "Sum of intergers")
# Test(test_sort, "Test sort", True)
# Test(test_fibo, "Test Fibonnaci")
