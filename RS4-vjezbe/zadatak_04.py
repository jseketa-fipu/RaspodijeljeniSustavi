# zadatak 4: simulacija autentifikacije korisnika
import asyncio
from typing import Dict

# Kako se ponaša asyncio.gather() kada se dogodi iznimka u jednoj od korutina?
# if the asyncio.gather is kept at its default with return_exception=False
# the first exception is propagated, and all the other coroutines are cancelled
# if still pending
#
# if I want to collect exceptions instead of panicking out of it,
# use asyncio.gather(*task_list, return_exceptions=True)

korisnici: Dict[str, str] = {
    "korisnik1": "lozinka1",
    "korisnik2": "lozinka2",
    "korisnik3": "lozinka3",
}

# 5 users: some valid, some invalid
attempts = [
    ("korisnik1", "lozinka1"),  # valid
    ("korisnik2", "wrong"),  # invalid
    ("korisnikX", "lozinka3"),  # invalid (user not in dict)
    ("korisnik3", "lozinka3"),  # valid
    ("korisnik2", "lozinka2"),  # valid
]


async def autentifikacija(
    korisnicko_ime: str, lozinka: str, service_down: bool = False
) -> bool:
    """
    Simulate slow I/O (2 seconds) and then check username/password.
    Return True if correct, otherwise raise ValueError.
    """
    # simulate timeout
    # not really happy with this because of the race condition
    # between this raise and wait_for raise
    if service_down:
        await asyncio.sleep(3)
        raise TimeoutError("Service is down.")

    print(f"Starting auth for {korisnicko_ime}")
    await asyncio.sleep(2)

    if korisnici.get(korisnicko_ime) == lozinka:
        print(f"Auth OK for {korisnicko_ime}")
        return True

    print(f"Auth FAILED for {korisnicko_ime}")
    raise ValueError(f"Invalid credentials for {korisnicko_ime}")


async def main() -> None:
    # tasks are already running here
    tasks = [
        asyncio.wait_for(autentifikacija(user, password, True), timeout=3.1)
        for user, password in attempts
    ]
    # if the timeout error occurs, there is a race condition between
    # the TimeoutError exception raised in the coroutine and the one
    # that the asyncio.wait_for raises.
    # only happens if the wait timeout and sleep are the same value

    # gathering the results
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print("Results:", results)


if __name__ == "__main__":
    asyncio.run(main())
