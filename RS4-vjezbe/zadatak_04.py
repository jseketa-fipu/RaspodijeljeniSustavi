# zadatak 4: simulacija autentifikacije korisnika
import asyncio
from typing import Dict

# Kako se ponaša asyncio.gather() kada se dogodi iznimka u jednoj od korutina?
# if the asyncio.gather is kept at its default with return_exception=False
# the firs exception is propagated, and all the other coroutines are cancelled
# if still pending
# if I want to collect exceptions instead of panicking out of it,
# use asyncio.gather(*task_list, return_exceptions=True)

korisnici: Dict[str, str] = {
    "korisnik1": "lozinka1",
    "korisnik2": "lozinka2",
    "korisnik3": "lozinka3",
}


async def autentifikacija(korisnicko_ime: str, lozinka: str) -> bool:
    """
    Simulate slow I/O (2 seconds) and then check username/password.
    Return True if correct, otherwise raise ValueError.
    """
    print(f"Starting auth for {korisnicko_ime}")
    await asyncio.sleep(2)

    if korisnici.get(korisnicko_ime) == lozinka:
        print(f"Auth OK for {korisnicko_ime}")
        return True

    print(f"Auth FAILED for {korisnicko_ime}")
    raise ValueError(f"Invalid credentials for {korisnicko_ime}")


async def main_basic() -> None:
    # 5 users: some valid, some invalid
    attempts = [
        ("korisnik1", "lozinka1"),  # valid
        ("korisnik2", "wrong"),  # invalid
        ("korisnikX", "lozinka3"),  # invalid (user not in dict)
        ("korisnik3", "lozinka3"),  # valid
        ("korisnik2", "lozinka2"),  # valid
    ]

    coros = [autentifikacija(u, p) for u, p in attempts]

    try:
        results = await asyncio.gather(*coros)
        print("Results:", results)
    except Exception as e:
        print("asyncio.gather raised:", repr(e))


if __name__ == "__main__":
    asyncio.run(main_basic())
