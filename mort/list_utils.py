from typing import List, Callable, Any, Optional


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
    if not isinstance(args, tuple):
        args = (args,)

    return func(*args, **kwargs)


def some(predicate: Callable[..., bool], l: List[Any]) -> bool:
    for el in l:
        if apply(predicate, el):
            return True
    return False


def every(predicate: Callable[..., bool], l: List[Any]) -> bool:
    if not l:
        return False

    for el in l:
        if not apply(predicate, el):
            return False
    return True


def first(predicate: Callable[..., bool], l: List[Any]) -> Optional[Any]:
    for el in l:
        if apply(predicate, el):
            return el
    return None
