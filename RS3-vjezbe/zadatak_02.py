import asyncio
from perf.timer import Timer


# full steps to run a coroutine
# 1. define an async function with async def function_name
# 2. gather it with others with await asyncio.gather(function_name()) in an
#   async def function
# 3. execute with asyncio.run(execute_all()) - execute_all is a function
# that gathered the coroutines earlier
# timing is a bit bulky, look into decorator, or context manager for it


baza_korisnika: list[dict[str, str]] = [
    {"korisnicko_ime": "mirko123", "email": "mirko123@gmail.com"},
    {"korisnicko_ime": "ana_anic", "email": "aanic@gmail.com"},
    {"korisnicko_ime": "maja_0x", "email": "majaaaaa@gmail.com"},
    {"korisnicko_ime": "zdeslav032", "email": "deso032@gmail.com"},
]

baza_proizvoda: list[dict[str, str | int]] = [
    {"barkod_proizvoda": 46730, "ime_proizvoda": "Mlijeko 1L"},
    {"barkod_proizvoda": 84551, "ime_proizvoda": "Vindija sok 0.5L"},
]


async def fetch_user_data() -> list[dict[str, str]]:
    await asyncio.sleep(3)

    return baza_korisnika


async def fetch_product_data() -> list[dict[str, str | int]]:
    await asyncio.sleep(5)

    return baza_proizvoda


async def execute_all() -> None:
    data = await asyncio.gather(fetch_user_data(), fetch_product_data())
    print(data)


# with Timer ... as t - creates an object t
with Timer("time execute all") as timer:
    asyncio.run(execute_all())
