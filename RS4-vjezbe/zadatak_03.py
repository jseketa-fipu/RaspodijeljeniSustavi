# zadatak 3: mix_dog_cat_facts
# dog api format:
# {"data": [{"id": UUID, "type": "fact", "attributes":{"body": str}}]}
import asyncio
import aiohttp
from typing import Iterator, Any

API_DATA = {
    "dog": {"url": "https://dogapi.dog/api/v2/facts", "key": "body"},
    "cat": {"url": "https://catfact.ninja/fact", "key": "fact"},
}


def find_key(obj: Any, key: str) -> Iterator[Any]:
    """
    Recursively search for all values associated with `key`
    in a nested structure of dicts/lists.
    """
    if isinstance(obj, dict):
        if key in obj:
            yield obj[key]
        for value in obj.values():
            yield from find_key(value, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from find_key(item, key)


async def get_facts(session: aiohttp.ClientSession, api_format: dict[str, str]) -> Any:
    async with session.get(api_format["url"]) as resp:
        resp.raise_for_status()
        data = await resp.json(content_type=None)

        # only the value of the 'body' key is relevant
        return next(find_key(data, api_format["key"]), None)


async def mix_facts(facts: tuple[list[str], list[str]]) -> list[str]:
    dog_facts, cat_facts = facts

    mixed_list: list[str] = []

    for dog_fact, cat_fact in zip(dog_facts, cat_facts):
        mixed_list.append(dog_fact if len(dog_fact) > len(cat_fact) else cat_fact)

    return mixed_list


async def main() -> list[str]:
    async with aiohttp.ClientSession() as session:
        dog_facts_tasks = [get_facts(session, API_DATA["dog"]) for _ in range(5)]
        cat_facts_tasks = [get_facts(session, API_DATA["cat"]) for _ in range(5)]
        dog_cat_facts = await asyncio.gather(*dog_facts_tasks, *cat_facts_tasks)

    return await mix_facts((dog_cat_facts[:5], dog_cat_facts[5:]))


if __name__ == "__main__":
    results = asyncio.run(main())
    print("Mixane činjenice o psima i mačkama:")
    for result in results:
        print(result)
