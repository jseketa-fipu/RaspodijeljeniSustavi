import random
import asyncio
from perf.timer import Timer


async def provjeri_parnost(number: int) -> None:
    await asyncio.sleep(2)
    formatted_output = f"Broj {number} je {'paran' if number % 2 == 0 else 'neparan'}."

    print(formatted_output)


async def main() -> None:
    random_numbers = [random.randint(1, 100) for i in range(10)]
    tasks = [asyncio.create_task(provjeri_parnost(number)) for number in random_numbers]

    await asyncio.gather(*tasks)


if __name__ == "__main__":

    with Timer("More then 2 seconds, but not for a lot: ") as timer:
        asyncio.run(main())
