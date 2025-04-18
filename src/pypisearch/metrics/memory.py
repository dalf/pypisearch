from contextlib import contextmanager
from dataclasses import dataclass

import psutil


def get_memory_uss(pid: int | None = None):
    """Return USS memory for a PID

    From https://stackoverflow.com/questions/22372960/is-this-explanation-about-vss-rss-pss-uss-accurate :

    * VSS (reported as VSZ from ps) is the total accessible address space of a process.
    * RSS is the total memory actually held in RAM for a process.
      RSS is not an accurate representation of the memory usage for a single process.
    * PSS differs from RSS in that it reports the proportional size of its shared libraries
    * USS is the total private memory for a proces

    See also https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
    """
    try:
        return int(psutil.Process(pid).memory_full_info().uss)
    except psutil.NoSuchProcess:
        return -1


def get_smaps_summary(pid: int | None = None):
    heap = 0
    anon = 0
    total = 0
    current_region = None

    if pid is None:
        pid = psutil.Process().pid

    with open(f"/proc/{pid}/smaps", "r") as f:
        for line in f:
            if line.startswith("Size:"):
                size = int(line.split()[1])
                total += size
            elif line.startswith("Anonymous:"):
                anon += int(line.split()[1])
            elif "[heap]" in line:
                current_region = "heap"
            elif line.strip() == "":
                current_region = None

            if current_region == "heap" and line.startswith("Size:"):
                heap += int(line.split()[1])

    return {"heap_kb": heap, "anonymous_mmaps_kb": anon, "total_mapped_kb": total}


@dataclass
class MemoryMeasure:
    heap_kb: int = 0
    anonymous_mmaps_kb: int = 0
    total_mapped_kb: int = 0
    uss_kb: int = 0
    count: int = 0

    def add_measure(self, heap_kb: int, anonymous_mmaps_kb: int, total_mapped_kb: int, uss_kb: int):
        self.heap_kb += heap_kb
        self.anonymous_mmaps_kb += anonymous_mmaps_kb
        self.total_mapped_kb += total_mapped_kb
        self.uss_kb += uss_kb
        self.count += 1

    def __repr__(self):
        return f"<{self.__class__.__name__} USS={self.uss_kb:6} KB, heap={self.heap_kb:6} KB, anonymous_mmaps={self.anonymous_mmaps_kb:6} KB, total_mapped={self.total_mapped_kb:6} KB, count={self.count:3}>"


class MemoryWatch:
    def __init__(self):
        self.measures: dict[str, MemoryMeasure] = {}

    @contextmanager
    def measure(self, name: str):
        memory_before_detail = get_smaps_summary()
        memory_before = get_memory_uss()
        yield
        memory_after = get_memory_uss()
        memory_after_detail = get_smaps_summary()

        result = {k: v - memory_before_detail[k] for k, v in memory_after_detail.items()}
        result["uss_kb"] = (memory_after - memory_before) // 1024

        if name not in self.measures:
            self.measures[name] = MemoryMeasure()
        self.measures[name].add_measure(**result)

    def __getitem__(self, key):
        return self.measures[key]

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.measures.items())
