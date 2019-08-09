from collections import namedtuple
from greenlet import greenlet


_Result = namedtuple('Result', ['value'])


class GreenletGenerator(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._next_result = None
        self._func_greenlet = greenlet(func)  # Stays the same greenlet
        self._consume_greenlet = None  # Changes on each call to `next`

    def yield_(self, item):
        self._next_result = _Result(item)
        self._consume_greenlet.switch()

    def _consume_next_result(self):
        self._func_greenlet.switch(*self.args, **self.kwargs)
        result = self._next_result
        self._next_result = None
        return result

    def next(self):
        self._consume_greenlet = greenlet(self._consume_next_result)
        result = self._consume_greenlet.switch()
        if result is None:
            raise StopIteration()
        return result.value

    __next__ = next

    def __iter__(self):
        return self

    def __repr__(self):
        return '<Greengen of {}>'.format(self.func)