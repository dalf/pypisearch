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
        pid = psutil.Process(pid).pid

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
