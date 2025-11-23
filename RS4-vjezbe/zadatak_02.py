# zadatak 02 - filter_cat_facts
# url: https://catfact.ninja/fact
# format of the api is
# {"fact": str, "length": int}
import re
import asyncio
import aiohttp
from typing import Any

CAT_API_URL = "https://catfact.ninja/fact"

# create a search pattern for cat/cats
# \b signifies a word boundary
# s? signifies with or without s
# IGNORECASE is there so I don't have to use .lower()
pattern = re.compile(r"\bcats?\b", re.IGNORECASE)


async def get_cat_fact(session: aiohttp.ClientSession) -> Any:
    async with session.get(CAT_API_URL) as resp:
        resp.raise_for_status()

        # only the value of the 'fact' key is relevant
        return (await resp.json(content_type=None)).get("fact")


async def filter_cat_facts(facts: list[str]) -> list[str]:
    # let's do list comprehension for exercise
    return [fact for fact in facts if pattern.search(fact)]


async def main() -> list[str]:

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_cat_fact(session)) for _ in range(20)]
        results: list[str] = await asyncio.gather(*tasks)

    return await filter_cat_facts(results)


if __name__ == "__main__":
    filtered_for_print: list[str] = asyncio.run(main())
    print(filtered_for_print)
    print(len(filtered_for_print))
