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
