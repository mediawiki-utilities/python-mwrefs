import functools
import collections
import sys
import regex as re


Diff = collections.namedtuple("Diff", "action data")


def diff(previous, current):
    # previous = [ref.text for ref in previous]
    # current = [ref.text for ref in current]

    added = set(current) - set(previous)
    removed = set(previous) - set(current)

    diff = (
        [Diff('added', el) for el in added]
        + [Diff('removed', el) for el in removed]
    )

    return diff


# https://github.com/shazow/unstdlib.py/blob/master/unstdlib/standard/list_.py#L149
def listify(fn=None, wrapper=list):
    """
    A decorator which wraps a function's return value in ``list(...)``.

    Useful when an algorithm can be expressed more cleanly as a generator but
    the function should return an list.

    Example::

        >>> @listify
        ... def get_lengths(iterable):
        ...     for i in iterable:
        ...         yield len(i)
        >>> get_lengths(["spam", "eggs"])
        [4, 4]
        >>>
        >>> @listify(wrapper=tuple)
        ... def get_lengths_tuple(iterable):
        ...     for i in iterable:
        ...         yield len(i)
        >>> get_lengths_tuple(["foo", "bar"])
        (3, 3)
    """
    def listify_return(fn):
        @functools.wraps(fn)
        def listify_helper(*args, **kw):
            return wrapper(fn(*args, **kw))
        return listify_helper
    if fn is None:
        return listify_return
    return listify_return(fn)


def iter_with_prev(iterable):
    last = None
    for el in iterable:
        yield last, el
        last = el


def dot(num=None):
    if not num:
        what = '.'
    elif num < 10:
        what = str(num)
    else:
        what = '>'
    print(what, end='', file=sys.stderr, flush=True)


def log(*args):
    first, *rest = args
    print('\n' + str(first), *rest, end='', file=sys.stderr, flush=True)


def remove_comments(source):
    pattern = re.compile(r'<!--(.*?)-->', re.MULTILINE | re.DOTALL)
    return pattern.sub('', source)


def has_next(peekable):
    try:
        peekable.peek()
        return True
    except StopIteration:
        return False
