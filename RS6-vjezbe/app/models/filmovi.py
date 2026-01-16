import re
from typing import Any, Literal, Optional

from pydantic import BaseModel, field_validator


class PersonName(BaseModel):
    name: str
    surname: str


class Actor(PersonName):
    pass


class Writer(PersonName):
    pass


class Film(BaseModel):
    Title: str
    Year: int
    Rated: str
    Released: Optional[str] = None
    Runtime: int
    Genre: str
    Director: Optional[str] = None
    Writer: list[Writer]
    Actors: list[Actor]
    Plot: str
    Language: str
    Country: str
    Awards: Optional[str] = None
    Poster: Optional[str] = None
    Metascore: Optional[int] = None
    imdbRating: float
    imdbVotes: int
    imdbID: str
    Type: Literal["movie", "series"]
    Response: Optional[str] = None
    Images: Optional[list[str]] = None
    totalSeasons: Optional[int] = None
    DVD: Optional[str] = None
    BoxOffice: Optional[str] = None
    Production: Optional[str] = None
    Website: Optional[str] = None

    @field_validator("Images", mode="before")
    def normalize_images(cls, value: Any) -> list[str]:
        if value in (None, ""):
            return []
        if isinstance(value, list):
            value_list: list[Any] = value
            images: list[str] = []
            for item in value_list:
                if not isinstance(item, str):
                    raise ValueError("Svaka slika mora biti string.")
                images.append(item)
            return images
        raise ValueError("Images mora biti lista stringova.")

    @field_validator("Runtime", mode="before")
    def parse_runtime(cls, value: Any) -> int:
        if isinstance(value, int):
            runtime = value
        else:
            match = re.search(r"(\d+)", str(value))
            if not match:
                raise ValueError("Runtime mora sadržavati broj minuta.")
            runtime = int(match.group(1))
        if runtime <= 0:
            raise ValueError("Runtime mora biti veći od 0.")
        return runtime

    @field_validator("imdbVotes", mode="before")
    def parse_votes(cls, value: Any) -> int:
        if isinstance(value, int):
            votes = value
        else:
            digits = str(value).replace(",", "").strip()
            votes = int(digits)
        if votes <= 0:
            raise ValueError("Broj glasova mora biti veći od 0.")
        return votes

    @field_validator("imdbRating", mode="before")
    def parse_rating(cls, value: Any) -> float:
        if isinstance(value, (int, float)):
            rating = float(value)
        else:
            rating = float(str(value).strip())
        if rating < 0 or rating > 10:
            raise ValueError("Ocjena mora biti između 0 i 10.")
        return rating

    @field_validator("Year", mode="before")
    def parse_year(cls, value: Any) -> int:
        if isinstance(value, int):
            year = value
        else:
            digits = re.findall(r"\d{4}", str(value))
            if not digits:
                raise ValueError("Godina mora sadržavati godinu.")
            year = int(digits[0])
        if year <= 1900:
            raise ValueError("Godina mora biti veća od 1900.")
        return year

    @field_validator("Writer", "Actors", mode="before")
    def parse_people(cls, value: Any) -> list[dict[str, str]]:
        if isinstance(value, list):
            value_list: list[Any] = value
            people_from_list: list[dict[str, str]] = []
            for item in value_list:
                if isinstance(item, dict):
                    item_dict: dict[str, Any] = item
                    name = str(item_dict.get("name", "")).strip()
                    surname = str(item_dict.get("surname", "")).strip()
                else:
                    name = str(getattr(item, "name", "")).strip()
                    surname = str(getattr(item, "surname", "")).strip()
                if not name and not surname:
                    raise ValueError("Ime i prezime ne smiju biti prazni.")
                if not surname:
                    surname = name
                if not name:
                    name = surname
                people_from_list.append({"name": name, "surname": surname})
            return people_from_list
        people: list[dict[str, str]] = []
        for part in str(value).split(","):
            part = part.strip()
            if not part:
                continue
            if " " not in part:
                people.append({"name": part, "surname": part})
                continue
            first, rest = part.split(" ", 1)
            people.append({"name": first.strip(), "surname": rest.strip()})
        return people

    @field_validator("Metascore", mode="before")
    def parse_metascore(cls, value: Any) -> Optional[int]:
        if value in (None, ""):
            return None
        score = int(value)
        if score < 0:
            raise ValueError("Metascore mora biti nenegativan.")
        return score

    @field_validator("totalSeasons", mode="before")
    def parse_total_seasons(cls, value: Any) -> Optional[int]:
        if value in (None, ""):
            return None
        seasons = int(value)
        if seasons <= 0:
            raise ValueError("Broj sezona mora biti veći od 0.")
        return seasons
