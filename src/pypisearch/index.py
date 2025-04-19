import aiohttp
import msgspec
import pyzstd
import tantivy as tv
from tqdm import tqdm

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
    schema_builder.add_text_field("summary", stored=True, tokenizer_name=tokenizer_name)
    schema_builder.add_text_field("version", stored=True, tokenizer_name=tokenizer_name)
    schema_builder.add_text_field("package_url", stored=True, tokenizer_name="raw")
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
    write_index(await download_pypicache())


async def download_pypicache():
    async with aiohttp.ClientSession() as session, session.get("https://pypicache.repology.org/pypicache.json.zst") as response:
        print("Status:", response.status)
        print("Content-type:", response.headers["content-type"])
        return await response.read()


class DumpInfo(msgspec.Struct):
    name: str | None = None
    summary: str | None = None
    version: str | None = None
    package_url: str | None = None


class DumpEntry(msgspec.Struct):
    info: DumpInfo


def write_index(content: bytes):
    uncompressed_content = pyzstd.decompress(content).decode()
    entries = msgspec.json.decode(uncompressed_content, type=list[DumpEntry])

    schema = get_schema()

    idx = tv.Index(schema, path=INDEX_DIRECTORY)
    writer = idx.writer(128 << 20)
    for entry in tqdm(entries):
        writer.add_document(
            tv.Document(
                title=[entry.info.name or ""],
                summary=[entry.info.summary or ""],
                version=[entry.info.version or ""],
                package_url=[entry.info.package_url or ""],
            )
        )
    writer.commit()
    writer.wait_merging_threads()
