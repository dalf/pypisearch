import aiohttp
import whoosh
import whoosh.index
from whoosh.fields import *
from lxml import html

INDEX_DIRECTORY = "index"
INDEX: whoosh.index.Index | None = None


## SCHEMA ###################################################


def get_schema():
    return Schema(title=TEXT(stored=True))


## LOAD #####################################################


def load_index():
    global INDEX
    INDEX = whoosh.index.open_dir(INDEX_DIRECTORY)


def get_index() -> whoosh.index.Index:
    if INDEX is None:
        load_index()
    return INDEX


## DOWNLOAD & WRITE #########################################


async def download_index():
    write_index(await download_simple())


async def download_simple():
    async with aiohttp.ClientSession() as session, session.get("https://pypi.org/simple/") as response:
        print("Status:", response.status)
        print("Content-type:", response.headers["content-type"])
        return await response.text()


def write_index(content: str):
    doc = html.fromstring(content)
    links = doc.xpath("//a")
    names = []
    for a in links:
        # href = a.get("href")  # the URL (may be None)
        text = a.text_content().strip()  # the visible text, with surrounding whitespace removed
        names.append(text)

    ix = whoosh.index.create_in(INDEX_DIRECTORY, get_schema())
    writer = ix.writer()
    for doc_id, name in enumerate(names):
        writer.add_document(title=name)
    writer.commit()
