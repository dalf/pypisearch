import aiohttp
from lxml import html
from rust_fst import Set

PACKAGE_FILE = "packages.fst"
PACKAGE_NAMES: Set | None = None


## LOAD ###################################################


def load_dataset():
    global PACKAGE_NAMES
    PACKAGE_NAMES = Set(path=PACKAGE_FILE)


def get_dataset() -> Set:
    if PACKAGE_NAMES is None:
        load_dataset()
    return PACKAGE_NAMES


## DOWNLOAD & WRITE #######################################


async def download_dataset():
    write_dataset(await download_simple())


async def download_simple():
    async with aiohttp.ClientSession() as session, session.get("https://pypi.org/simple/") as response:
        print("Status:", response.status)
        print("Content-type:", response.headers["content-type"])
        return await response.text()


def write_dataset(content: str):
    global PACKAGE_NAMES
    doc = html.fromstring(content)
    links = doc.xpath("//a")
    names = []
    for a in links:
        # href = a.get("href")  # the URL (may be None)
        text = a.text_content().strip()  # the visible text, with surrounding whitespace removed
        norm_text = normalize(text)
        names.append(norm_text)

    names = sorted(names)
    PACKAGE_NAMES = Set.from_iter(names, PACKAGE_FILE)


def normalize(text):
    return text.lower()
