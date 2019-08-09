import pytest
import greengen
from greengen.api import NoCurrentGreengenException


@greengen.greengen
def simple_greengen(n):
    middle_func(n, n * 2)


def middle_func(x, y):
    for num in range(x, y):
        yielding_func(num)


def yielding_func(num):
    greengen.yield_('hello {}'.format(num))


@greengen.greengen
def while_true_greengen():
    while True:
        greengen.yield_('a')
        greengen.yield_('b')


@greengen.greengen
def nested_greengen():
    for n in range(3):
        greengen.yield_('results for {}:'.format(n))
        for res in simple_greengen(n):
            greengen.yield_(res)


@greengen.greengen
def exception_greengen():
    for x in [1, 0]:
        greengen.yield_(1 / x)


@pytest.mark.parametrize(('param', 'expected_results'), [
    (0, []),
    (1, ['hello 1']),
    (2, ['hello 2', 'hello 3']),
])
def test_simple_greengen(param, expected_results):
    gen = simple_greengen(param)
    assert list(gen) == expected_results


def test_nested_greengen():
    gen = nested_greengen()
    assert list(gen) == ['results for 0:', 'results for 1:', 'hello 1', 'results for 2:', 'hello 2', 'hello 3']


@pytest.mark.timeout(3)
def test_greengen_evaluates_lazily():
    gen = while_true_greengen()
    assert next(gen) == 'a'
    assert next(gen) == 'b'
    assert next(gen) == 'a'


def test_greengen_can_be_traversed_multiple_times():
    gen1 = simple_greengen(1)
    gen2 = simple_greengen(1)
    assert list(gen1) == list(gen2) == ['hello 1']


def test_yield_exception_when_outside_greengen():
    with pytest.raises(NoCurrentGreengenException):
        greengen.yield_(1)


def test_greengen_propagating_exceptions():
    gen = exception_greengen()
    assert next(gen) == 1
    with pytest.raises(ZeroDivisionError):
        next(gen)
