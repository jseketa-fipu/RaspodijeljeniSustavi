# zadatak 5: Pretvorba sinkronog koda u asinkroni
import asyncio
import aiohttp


async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        resp.raise_for_status()

        return await resp.text()


async def main() -> None:
    urls = ["https://example.com", "https://httpbin.org/get", "https://api.github.com"]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    for url, result in zip(urls, results):
        print(f"Fetched {len(result)} characters from {url}")


if __name__ == "__main__":
    asyncio.run(main())
