from contextlib import contextmanager
import decorator
from greengen.generator import GreenletGenerator

_current_greengen = None


class NoCurrentGreengenException(SyntaxError):
    pass


def yield_(item):
    if _current_greengen is None:
        raise NoCurrentGreengenException('yield outside greengen')
    _current_greengen.yield_(item)


@decorator.decorator
def greengen(func, *args, **kwargs):
    curr_greengen = GreenletGenerator(func, *args, **kwargs)
    try:
        # Set the current greengen, so that calls to `yield_` will yield to this greengen.
        with _swap_current_greengen(curr_greengen) as prev_greengen:
            for item in curr_greengen:
                # We need to temporarily swap back to the previous greengen, so that nested greengens' calls to `yield_`
                # will yield to the correct greengen, and not the inner greengen.
                with _swap_current_greengen(prev_greengen):
                    yield item
    finally:
        # We have to call the `__del__` explicitly to prevent memory leaks caused by circular references.
        curr_greengen.__del__()


@contextmanager
def _swap_current_greengen(new_greengen):
    global _current_greengen
    backup = _current_greengen
    _current_greengen = new_greengen
    try:
        yield backup
    finally:
        _current_greengen = backup
