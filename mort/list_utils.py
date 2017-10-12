from typing import List, Callable, Any


def iterable(l) -> bool:
    return hasattr(l, '__iter__')


def apply(func: Callable, args=None, kwargs=None):
    """Call a callable object with positional arguments taken from the
    tuple args, and keyword arguments taken from the optional dictionary
    kwargs; return its results.
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    if not iterable(args):
        args = (args, )

    return func(*args, **kwargs)


def some(l: List[Any], predicate: Callable[..., bool]) -> bool:
    for el in l:
        if apply(predicate, el):
            return True
    return False
