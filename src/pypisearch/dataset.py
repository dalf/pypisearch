import aiohttp
import marisa_trie
from lxml import html

MARISA_FILENAME = "packages.marisa"
MARISA_TRIE: marisa_trie.Trie | None = None


## LOAD ###################################################


def load_dataset():
    global MARISA_TRIE
    MARISA_TRIE = marisa_trie.Trie()
    # MARISA_TRIE.load(PACKAGE_FILE)
    MARISA_TRIE.mmap(MARISA_FILENAME)


def get_dataset() -> marisa_trie.Trie:
    if MARISA_TRIE is None:
        load_dataset()
    return MARISA_TRIE


## DOWNLOAD & WRITE #######################################


async def download_dataset():
    write_dataset(await download_simple())


async def download_simple():
    async with aiohttp.ClientSession() as session, session.get("https://pypi.org/simple/") as response:
        print("Status:", response.status)
        print("Content-type:", response.headers["content-type"])
        return await response.text()


def write_dataset(content: str):
    global MARISA_TRIE
    doc = html.fromstring(content)
    links = doc.xpath("//a")
    names = []
    for a in links:
        text = a.text_content().strip()
        norm_text = normalize(text)
        names.append(norm_text)

    names = sorted(names)
    MARISA_TRIE = marisa_trie.Trie(names)

    # Save the trie to disk using pickle
    MARISA_TRIE.save(MARISA_FILENAME)


def normalize(text):
    return text.lower()
