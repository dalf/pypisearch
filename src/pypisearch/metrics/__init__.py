from contextlib import contextmanager

from .memory import MemoryWatch
from .time import TimeWatch

__all__ = ["MemoryWatch", "TimeWatch"]


MEMORY_WATCH = MemoryWatch()
TIME_WATCH = TimeWatch()


@contextmanager
def measure(name: str):
    with MEMORY_WATCH.measure(name), TIME_WATCH.measure(name):
        yield


def get_measure(name: str):
    return (TIME_WATCH[name], MEMORY_WATCH[name])
