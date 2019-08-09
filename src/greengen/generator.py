from collections import namedtuple
from greenlet import greenlet


_ItemWrapper = namedtuple('_ItemWrapper', ['value'])


class GreenletGenerator(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._next_item = None
        self._func_greenlet = None  # Will stay the same greenlet
        self._consume_greenlet = None  # Will change on each call to `next`

    def yield_(self, item):
        self._next_item = _ItemWrapper(item)
        self._consume_greenlet.switch()

    def _consume_next_item(self):
        if self._func_greenlet is None:
            self._func_greenlet = greenlet(self.func)
        self._func_greenlet.switch(*self.args, **self.kwargs)
        wrapped_item = self._next_item
        self._next_item = None
        return wrapped_item

    def next(self):
        self._consume_greenlet = greenlet(self._consume_next_item)
        wrapped_item = self._consume_greenlet.switch()
        if wrapped_item is None:
            raise StopIteration()
        return wrapped_item.value

    __next__ = next

    def __iter__(self):
        return self

    def __repr__(self):
        return '<GreenletGenerator: {}>'.format(self.func)

    def __del__(self):
        self._consume_greenlet = None
        self._func_greenlet = None
