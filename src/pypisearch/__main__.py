import asyncio

import aiohttp
import click
import uvloop

from .dataset import download_dataset, get_dataset
from .metrics import StopWatch
from .utils import get_memory_uss

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


async def async_search(query: str):
    norm_query = query.lower()

    package_name_list = list(get_dataset().search_re(norm_query + ".*"))
    if not package_name_list:
        package_name_list = list(get_dataset().search(norm_query, 2))
    if not package_name_list:
        package_name_list = list(get_dataset().search_re(".*" + norm_query + ".*"))
    details = await fetch_all(package_name_list)
    for package_name, detail in details.items():
        print(detail.get("info", {}).get("name", package_name))
        if "info" in detail:
            print("   summary:", detail["info"]["summary"])
            print("   version:", detail["info"]["version"])


@click.group()
def cli():
    """My CLI app."""
    pass


@cli.command()
def download():
    asyncio.run(download_dataset())


@cli.command()
@click.argument("text", type=str)
def search(text: str):
    sw = StopWatch()
    with sw.measure("load"):
        memory_before = get_memory_uss()
        get_dataset()
        memory_after = get_memory_uss()

    with sw.measure("query"):
        asyncio.run(async_search(text))

    print("--------------------")
    print("cputime=", sw.get_cputime_dict())
    print("runtime=", sw.get_runtime_dict())
    print("memory usage for dataset =", memory_after - memory_before, "bytes")


if __name__ == "__main__":
    cli()
