import asyncio
from perf.timer import Timer
from typing import TypedDict


class KorisnikType(TypedDict):
    korisnicko_ime: str
    email: str


baza_korisnika: list[KorisnikType] = [
    {"korisnicko_ime": "mirko123", "email": "mirko123@gmail.com"},
    {"korisnicko_ime": "ana_anic", "email": "aanic@gmail.com"},
    {"korisnicko_ime": "maja_0x", "email": "majaaaaa@gmail.com"},
    {"korisnicko_ime": "zdeslav032", "email": "deso032@gmail.com"},
]


class LozinkaType(TypedDict):
    korisnicko_ime: str
    lozinka: str


class WantedUserType(KorisnikType, LozinkaType):  # type: ignore
    pass


baza_lozinka: list[LozinkaType] = [
    {"korisnicko_ime": "mirko123", "lozinka": "lozinka123"},
    {"korisnicko_ime": "ana_anic", "lozinka": "super_teska_lozinka"},
    {"korisnicko_ime": "maja_0x", "lozinka": "s324SDFfdsj234"},
    {"korisnicko_ime": "zdeslav032", "lozinka": "deso123"},
]


# authentication = who am i
async def authenticate(user: WantedUserType) -> None:
    # simulate load by waiting for 3 seconds
    await asyncio.sleep(3)
    subset = {key: user[key] for key in ("korisnicko_ime", "email")}  # type: ignore
    for user_db in baza_korisnika:
        if subset == user_db:
            print("Korisnik postoji!")
            await authorize(user_db, user["lozinka"])
            return None

    print(f"Korisnik {user['korisnicko_ime']} nije pronađen. ")

    return None


# authorization = what can i do
async def authorize(user: KorisnikType, lozinka: str) -> None:
    await asyncio.sleep(2)
    for user_db in baza_lozinka:
        if user["korisnicko_ime"] == user_db["korisnicko_ime"]:
            if lozinka == user_db["lozinka"]:
                print(f"Korisnik {user_db['korisnicko_ime']}: Autorizacija uspješna.")
                return None

    print(f"Korisnik {user['korisnicko_ime']}: Autorizacija neuspješna.")


user_to_be_checked: WantedUserType = {
    "korisnicko_ime": "mirko123",
    "email": "mirko123@gmail.com",
    "lozinka": "lozinka123",
}

if __name__ == "__main__":
    with Timer("Expected 5 seconds, got: ") as timer:
        asyncio.run(authenticate(user_to_be_checked))
