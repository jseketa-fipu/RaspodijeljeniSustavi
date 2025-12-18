import asyncio
import time
from aiohttp import ClientSession
from typing import Any


async def send_request(url: str, port: int) -> Any:
    async with ClientSession() as session:
        async with session.get(f"http://localhost:{port}{url}") as response:
            response.raise_for_status()
            # mypy insists that Dict[str, str] is not really OK
            # changed to simply return Any
            return await response.json()


async def main() -> None:
    print("Sekvencijalno slanje zahtjeva:")
    start = time.perf_counter()
    pozdrav_3s = await send_request("/pozdrav", 8081)
    pozdrav_4s = await send_request("/pozdrav", 8082)
    print("  8081 ->", pozdrav_3s)
    print("  8082 ->", pozdrav_4s)
    # expected 7 seconds
    print(f"  Trajanje: {time.perf_counter() - start:.2f}s\n")

    print("Konkurentno slanje zahtjeva:")
    start = time.perf_counter()
    pozdrav_3s, pozdrav_4s = await asyncio.gather(
        send_request("/pozdrav", 8081),
        send_request("/pozdrav", 8082),
    )
    print("  8081 ->", pozdrav_3s)
    print("  8082 ->", pozdrav_4s)
    # expected 4 seconds
    print(f"  Trajanje: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
