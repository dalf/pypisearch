import aiohttp
import tantivy as tv
from lxml import html

INDEX_DIRECTORY = "index"
INDEX: tv.Index | None = None


## SCHEMA ###################################################


def get_schema():
    schema_builder = tv.SchemaBuilder()
    tokenizer_name = "en_stem"  # "raw", "en_stem", "default"
    # "raw": get only exact match - 22M
    # "default": default tokenizer -
    # "en_stem": English tokenizer - 19M
    schema_builder.add_text_field("title", stored=True, tokenizer_name=tokenizer_name)
    return schema_builder.build()


## LOAD #####################################################


def load_index():
    global INDEX
    INDEX = tv.Index(get_schema(), path=INDEX_DIRECTORY)


def get_index() -> tv.Index:
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

    schema = get_schema()

    idx = tv.Index(schema, path=INDEX_DIRECTORY)
    writer = idx.writer(128 << 20)
    for doc_id, name in enumerate(names):
        writer.add_document(tv.Document(doc_id=doc_id, title=[name]))
    writer.commit()
    writer.wait_merging_threads()
