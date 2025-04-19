import asyncio

import click
import uvloop

from .index import download_index, get_index
from .metrics import get_measure, measure

uvloop.install()


def get_doc(d):
    return {
        "name": d["title"][0],
        "summary": d["summary"][0],
        "version": d["version"][0],
        "package_url": d["package_url"][0],
    }


def index_search(query: str) -> list[str]:
    index = get_index()
    searcher = index.searcher()
    query = index.parse_query(
        query,
        [
            "title",
            "summary",
        ],
    )
    result = searcher.search(query, 15).hits
    return [get_doc(searcher.doc(r[1])) for r in result]


async def async_search(query: str):
    with measure("query"):
        details = index_search(query)
    for detail in details:
        print(detail["name"])
        print("    summary     : ", detail["summary"])
        print("    version     : ", detail["version"])
        print("    project_url : ", detail["package_url"])


@click.group()
def cli():
    """My CLI app."""
    pass


@cli.command()
def download():
    asyncio.run(download_index())


@cli.command()
@click.argument("text", type=str)
def search(text: str):
    with measure("load"):
        get_index()

    with measure("search"):
        asyncio.run(async_search(text))

    print("--------------------")
    print("Load  ", get_measure("load"))
    print("Query ", get_measure("query"))
    print("Search", get_measure("search"))


if __name__ == "__main__":
    cli()
