from aiohttp import web
import hashlib

# In-memory "baza" korisnika (resetira se pri restartu kontejnera)
korisnici = [
    {
        "korisnicko_ime": "admin",
        "lozinka_hash": "8d43d8eb44484414d61a18659b443fbfe52399510da4689d5352bd9631c6c51b",
    },  # lozinka = "lozinka123"
    {
        "korisnicko_ime": "markoMaric",
        "lozinka_hash": "5493c883d2b943587ea09ab8244de7a0a88d331a1da9db8498d301ca315d74fa",
    },  # lozinka = "markoKralj123"
    {
        "korisnicko_ime": "ivanHorvat",
        "lozinka_hash": "a31d1897eb84d8a6952f2c758cdc72e240e6d6d752b33f23d15fd9a53ae7c302",
    },  # lozinka = "lllllllllllozinka_123"
    {
        "korisnicko_ime": "Nada000",
        "lozinka_hash": "492f3f38d6b5d3ca859514e250e25ba65935bcdd9f4f40c124b773fe536fee7d",
    },  # lozinka = "blablabla"
]


def hash_password(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def find_user(username: str) -> str | None:
    for user in korisnici:
        if user["korisnicko_ime"] == username:
            return user
    return None


# POST /register
# Body JSON: {"korisnicko_ime": "...", "lozinka": "..."}
async def register(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        return web.json_response(
            {"error": "Body of the request must be valid JSON."}, status=400
        )

    username = payload.get("korisnicko_ime")
    password = payload.get("lozinka")

    if not username or not password:
        return web.json_response(
            {"error": "Missing keys: korisnicko_ime and/or lozinka."},
            status=400,
        )

    if find_user(username) is not None:
        return web.json_response(
            {"error": "Username already taken."},
            status=409,
        )

    korisnici.append(
        {
            "korisnicko_ime": username,
            "lozinka_hash": hash_password(password),
        }
    )

    return web.json_response(
        {"message": "Korisnik registriran.", "korisnicko_ime": username},
        status=201,
    )


# POST /login
# Body JSON: {"korisnicko_ime": "...", "lozinka": "..."}
async def login(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        return web.json_response(
            {"error": "Body of the request must be valid JSON."}, status=400
        )

    username = payload.get("korisnicko_ime")
    password = payload.get("lozinka")

    if not username or not password:
        return web.json_response(
            {"error": "Missing keys: korisnicko_ime and/or lozinka."},
            status=400,
        )

    user = find_user(username)
    if user is None:
        return web.json_response(
            {"error": "User doesn't exist."},
            status=404,
        )

    if hash_password(password) != user["lozinka_hash"]:
        # why not just reporting that the password is wrong?
        # reducing attack surface, so that malevolent actors
        # don't know that they guessed the username and can
        # try to bruteforce the password.
        return web.json_response(
            {"error": "Wrong username or password."},
            status=401,
        )

    return web.json_response(
        {"message": "Login successful.", "korisnicko_ime": username},
        status=200,
    )


# # dockerize like this:
# docker build -t authapi .
# docker run --rm -p authapi

if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/register", register)
    app.router.add_post("/login", login)
    web.run_app(app, host="0.0.0.0", port=9000)
