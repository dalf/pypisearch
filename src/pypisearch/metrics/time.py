from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter, process_time
from typing import Dict


@dataclass
class TimeMeasure:
    runtime: float = 0.0
    cputime: float = 0.0
    count: int = 0

    def add_measure(self, runtime: float, cputime: float):
        self.runtime += runtime
        self.cputime += cputime
        self.count += 1

    def __repr__(self):
        return f"<{self.__class__.__name__} runtime={self.runtime:2.4f} cputime={self.cputime:2.4f} count={self.count:4}>"


class TimeWatch:
    def __init__(self) -> None:
        self.measures: Dict[str, TimeMeasure] = {}

    @contextmanager
    def measure(self, name: str):
        start_perf_counter = perf_counter()
        start_process_time = process_time()
        try:
            yield
        finally:
            runtime = perf_counter() - start_perf_counter
            cputime = process_time() - start_process_time
            if name not in self.measures:
                self.measures[name] = TimeMeasure()
            self.measures[name].add_measure(runtime, cputime)

    def __getitem__(self, name):
        return self.measures[name]

    def get_runtime_dict(self) -> Dict[str, float]:
        result = {name: rr.runtime for name, rr in self.measures.items()}
        result["total"] = self.get_total_runtime()
        return result

    def get_cputime_dict(self) -> Dict[str, float]:
        result = {name: rr.cputime for name, rr in self.measures.items()}
        result["total"] = self.get_total_cputime()
        return result

    def get_total_runtime(self) -> float:
        return sum(rr.runtime for rr in self.measures.values())

    def get_total_cputime(self) -> float:
        return sum(rr.cputime for rr in self.measures.values())

    def get_measure_count(self, name: str) -> float:
        if name not in self.measures:
            return 0
        return self.measures[name].count
