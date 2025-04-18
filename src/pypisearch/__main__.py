import asyncio

import aiohttp
import click
import uvloop

from .index import download_index, get_index
from .metrics import StopWatch
from .utils import get_memory_uss, get_smaps_summary

uvloop.install()


async def fetch_json(session: aiohttp.ClientSession, package_name: str) -> dict:
    """Fetch JSON content from a URL using the provided aiohttp session."""
    try:
        url = f"https://pypi.org/pypi/{package_name.lower().replace('-', '_')}/json"
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return {}


async def fetch_all(package_name_list: list[str]) -> dict[str, dict]:
    """Fetch JSON from all URLs concurrently and return a mapping of URL to JSON content."""
    results: dict[str, dict] = {}
    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Create a list of tasks for all URLs
        tasks = {package_name: asyncio.create_task(fetch_json(session, package_name)) for package_name in package_name_list}

        # Await tasks and collect results
        for package_name, task in tasks.items():
            results[package_name] = await task

    return results


def index_search(query: str) -> list[str]:
    index = get_index()
    searcher = index.searcher()
    query = index.parse_query(
        query,
        [
            "title",
        ],
    )
    result = searcher.search(query, 15).hits
    return [searcher.doc(r[1])["title"][0] for r in result]


async def async_search(query: str):
    package_name_list = index_search(query)
    details = await fetch_all(package_name_list)
    for package_name, detail in details.items():
        print(detail.get("info", {}).get("name", package_name))
        if "info" in detail:
            print("    summary     : ", detail["info"]["summary"])
            print("    version     : ", detail["info"]["version"])
            print("    project_url : ", detail["info"]["project_url"])


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
    sw = StopWatch()
    memory_before_detail = get_smaps_summary()
    memory_before = get_memory_uss()
    with sw.measure("load"):
        get_index()

    with sw.measure("query"):
        asyncio.run(async_search(text))
    memory_after = get_memory_uss()
    memory_after_detail = get_smaps_summary()

    print("--------------------")
    print("cputime=", sw.get_cputime_dict())
    print("runtime=", sw.get_runtime_dict())
    print("memory usage for loading the index =", memory_after - memory_before, "bytes")
    memdiff = {k: v - memory_before_detail[k] for k, v in memory_after_detail.items()}
    print("memory diff=", memdiff)


if __name__ == "__main__":
    cli()
