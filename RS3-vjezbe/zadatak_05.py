import asyncio
from typing import TypedDict
from perf.timer import Timer


class SensitiveDataType(TypedDict):
    prezime: str
    broj_kartice: str
    CVV: str


async def secure_data(sensitive_data: SensitiveDataType) -> SensitiveDataType:
    await asyncio.sleep(3)
    sensitive_data["broj_kartice"] = str(hash(sensitive_data["broj_kartice"]))
    sensitive_data["CVV"] = str(hash(sensitive_data["CVV"]))

    return sensitive_data


sens_data: list[SensitiveDataType] = [
    {"prezime": "Peric", "broj_kartice": "22", "CVV": "138"},
    {"prezime": "Maric", "broj_kartice": "22", "CVV": "138"},
    {"prezime": "Nozic", "broj_kartice": "22", "CVV": "138"},
]


async def main() -> None:

    tasks = [asyncio.create_task(secure_data(data)) for data in sens_data]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == "__main__":
    with Timer("Wait for 3 seconds: ") as timer:
        asyncio.run(main())
