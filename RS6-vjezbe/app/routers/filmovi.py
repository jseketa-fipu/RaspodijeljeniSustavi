import json
from pathlib import Path
from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException

from app.models.filmovi import Film

router = APIRouter(prefix="/filmovi", tags=["filmovi-service"])


def _load_filmovi() -> List[Film]:
    data_path = Path(__file__).resolve().parent.parent / "data" / "filmovi.json"
    with data_path.open(encoding="utf-8") as file:
        raw = json.load(file)
    return [Film(**item) for item in raw]


FILMOVI_DATA = _load_filmovi()


@router.get("/", response_model=List[Film])
def list_all_films(
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    film_type: Optional[Literal["movie", "series"]] = None,
) -> list[Film]:
    if min_year is not None and min_year < 1900:
        raise HTTPException(
            status_code=400, detail="Minimalna godina mora biti veća od 1900."
        )
    if max_year is not None and max_year < 1900:
        raise HTTPException(
            status_code=400, detail="Maksimalna godina mora biti veća od 1900."
        )
    if min_rating is not None and (min_rating < 0 or min_rating > 10):
        raise HTTPException(
            status_code=400, detail="Minimalna ocjena mora biti između 0 i 10."
        )
    if max_rating is not None and (max_rating < 0 or max_rating > 10):
        raise HTTPException(
            status_code=400, detail="Maksimalna ocjena mora biti između 0 i 10."
        )
    if min_year and max_year and min_year > max_year:
        raise HTTPException(
            status_code=400, detail="Minimalna godina mora biti manja od maksimalne."
        )
    if min_rating and max_rating and min_rating > max_rating:
        raise HTTPException(
            status_code=400, detail="Minimalna ocjena mora biti manja od maksimalne."
        )

    rezultat = FILMOVI_DATA
    if min_year:
        rezultat = [film for film in rezultat if film.Year >= min_year]
    if max_year:
        rezultat = [film for film in rezultat if film.Year <= max_year]
    if min_rating:
        rezultat = [film for film in rezultat if film.imdbRating >= min_rating]
    if max_rating:
        rezultat = [film for film in rezultat if film.imdbRating <= max_rating]
    if film_type:
        rezultat = [film for film in rezultat if film.Type == film_type]
    return rezultat


@router.get("/pretraga/", response_model=Film)
def get_film_by_title(title: str) -> Film:
    normalized = title.strip().lower()
    for film in FILMOVI_DATA:
        if film.Title.lower() == normalized:
            return film
    raise HTTPException(
        status_code=404, detail="Film s traženim naslovom nije pronađen."
    )


@router.get("/{imdb_id}", response_model=Film)
def get_film_by_imdb(imdb_id: str) -> Film:
    for film in FILMOVI_DATA:
        if film.imdbID.lower() == imdb_id.lower():
            return film
    raise HTTPException(
        status_code=404, detail="Film s traženim imdbID-em nije pronađen."
    )
