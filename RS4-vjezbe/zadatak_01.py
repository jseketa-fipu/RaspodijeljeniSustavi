# zadatak 01 - fetch_users i izdvajanje podataka
import asyncio
import aiohttp
import itertools
from typing import Any
from perf.timer import Timer

API_URL = "https://jsonplaceholder.typicode.com/users"


async def fetch_users(session: aiohttp.ClientSession) -> Any:
    async with session.get(API_URL) as resp:
        resp.raise_for_status()

        return await resp.json(content_type=None)


async def main() -> None:

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_users(session)) for _ in range(5)]
        results: list[list[dict[str, Any]]] = await asyncio.gather(*tasks)

    # flatten List[List[user]] -> List[user]
    combined_users = list(itertools.chain.from_iterable(results))

    names = [user["name"] for user in combined_users]
    email_addresses = [user["email"] for user in combined_users]
    usernames = [user["username"] for user in combined_users]
    print(names)
    print(email_addresses)
    print(usernames)


if __name__ == "__main__":
    with Timer("Ukupno vrijeme izvodenja: ") as timer:
        asyncio.run(main())
