from typing import List, Optional, TypedDict
from fastapi import FastAPI, HTTPException, Query
from models import Car, CarCreate, CreateFilm, Film
from app.routers.filmovi import router as filmovi_router

app = FastAPI(
    title="RS6 FastAPI Zadaci",
    description="Raspodijeljeni sustavi - RS6 - FastAPI.",
)


class FilmEntry(TypedDict):
    id: int
    naziv: str
    genre: str
    godina: int


filmovi: List[FilmEntry] = [
    {"id": 1, "naziv": "Titanic", "genre": "drama", "godina": 1997},
    {"id": 2, "naziv": "Inception", "genre": "akcija", "godina": 2010},
    {
        "id": 3,
        "naziv": "The Shawshank Redemption",
        "genre": "drama",
        "godina": 1994,
    },
    {"id": 4, "naziv": "The Dark Knight", "genre": "akcija", "godina": 2008},
]

next_film_id = len(filmovi) + 1


@app.get("/filmovi", response_model=List[Film])
def get_filmovi(
    genre: Optional[str] = Query(None, description="Filtriranje po žanru."),
    min_godina: int = Query(
        2000, ge=1900, description="Minimalna godina proizvodnje filma."
    ),
) -> list[Film]:
    """
    Dohvat filmova s opcionalnim filtrima po žanru i minimalnoj godini.
    """
    rezultat = filmovi
    if genre:
        rezultat = [
            film for film in rezultat if film["genre"].lower() == genre.strip().lower()
        ]
    rezultat = [film for film in rezultat if film["godina"] >= min_godina]
    return [Film(**film) for film in rezultat]


@app.get("/filmovi/{film_id}", response_model=Film)
def get_film(film_id: int) -> Film:
    for film in filmovi:
        if film["id"] == film_id:
            return Film(**film)
    raise HTTPException(status_code=404, detail="Film nije pronađen.")


@app.post("/filmovi", response_model=Film, status_code=201)
def create_film(novi_film: CreateFilm) -> Film:
    global next_film_id
    film_entry: FilmEntry = {
        "id": next_film_id,
        "naziv": novi_film.naziv,
        "genre": novi_film.genre,
        "godina": novi_film.godina,
    }
    filmovi.append(film_entry)
    next_film_id += 1
    return Film(**film_entry)


cars: List[Car] = [
    Car(
        id=1,
        marka="Toyota",
        model="Corolla",
        godina_proizvodnje=2018,
        cijena=12000,
        boja="srebrna",
        cijena_pdv=15000,
    ),
    Car(
        id=2,
        marka="Volkswagen",
        model="Golf",
        godina_proizvodnje=2020,
        cijena=18000,
        boja="plava",
        cijena_pdv=22500,
    ),
    Car(
        id=3,
        marka="Tesla",
        model="Model 3",
        godina_proizvodnje=2022,
        cijena=42000,
        boja="bijela",
        cijena_pdv=52500,
    ),
]

next_car_id = len(cars) + 1


def _find_car(car_id: int) -> Optional[Car]:
    for car in cars:
        if car.id == car_id:
            return car
    return None


@app.get("/automobili", response_model=List[Car])
def list_cars(
    min_cijena: Optional[float] = Query(None, gt=0),
    max_cijena: Optional[float] = Query(None, gt=0),
    min_godina: Optional[int] = Query(None, gt=1960),
    max_godina: Optional[int] = Query(None, gt=1960),
) -> list[Car]:
    if min_cijena and max_cijena and min_cijena > max_cijena:
        raise HTTPException(
            status_code=400,
            detail="Minimalna cijena mora biti manja od maksimalne cijene.",
        )
    if min_godina and max_godina and min_godina > max_godina:
        raise HTTPException(
            status_code=400,
            detail="Minimalna godina mora biti manja od maksimalne godine.",
        )

    rezultat = cars
    if min_cijena:
        rezultat = [car for car in rezultat if car.cijena >= min_cijena]
    if max_cijena:
        rezultat = [car for car in rezultat if car.cijena <= max_cijena]
    if min_godina:
        rezultat = [car for car in rezultat if car.godina_proizvodnje >= min_godina]
    if max_godina:
        rezultat = [car for car in rezultat if car.godina_proizvodnje <= max_godina]
    return rezultat


@app.get("/automobili/{car_id}", response_model=Car)
def get_car(car_id: int) -> Car:
    car = _find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Automobil nije pronađen.")
    return car


@app.post("/automobili", response_model=Car, status_code=201)
def create_car(novi_auto: CarCreate) -> Car:
    global next_car_id
    for car in cars:
        if (
            car.marka.lower() == novi_auto.marka.lower()
            and car.model.lower() == novi_auto.model.lower()
            and car.godina_proizvodnje == novi_auto.godina_proizvodnje
            and car.boja.lower() == novi_auto.boja.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Automobil već postoji u bazi podataka.",
            )
    cijena_pdv = round(novi_auto.cijena * 1.25, 2)
    car = Car(id=next_car_id, cijena_pdv=cijena_pdv, **novi_auto.model_dump())
    cars.append(car)
    next_car_id += 1
    return car


app.include_router(filmovi_router)
