from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Tuple, TypedDict

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
)


class Film(BaseModel):
    id: int
    naziv: str
    genre: str
    godina: int = Field(..., ge=1900)


class CreateFilm(BaseModel):
    naziv: str
    genre: str
    godina: int = Field(..., ge=1900)


class Izdavac(BaseModel):
    naziv: str
    adresa: str


class Knjiga(BaseModel):
    naslov: str
    ime_autor: str
    prezime_autor: str
    godina_izdavanja: int = Field(default_factory=lambda: datetime.now().year, ge=1450)
    broj_stranica: int = Field(..., gt=0)
    izdavac: Izdavac


class Admin(BaseModel):
    ime: str
    prezime: str
    korisnicko_ime: str
    email: EmailStr
    ovlasti: List[Literal["dodavanje", "brisanje", "ažuriranje", "čitanje"]] = Field(
        default_factory=lambda: _default_ovlasti()
    )


def _default_ovlasti() -> (
    List[Literal["dodavanje", "brisanje", "ažuriranje", "čitanje"]]
):
    return []


class StolInfo(TypedDict):
    broj: int
    lokacija: str


class Jelo(BaseModel):
    id: int
    naziv: str
    cijena: float = Field(..., gt=0)


class RestaurantOrder(BaseModel):
    id: int
    kupac: str
    stol_info: StolInfo
    jela: List[Jelo]
    ukupna_cijena: float = Field(..., gt=0)

    @field_validator("ukupna_cijena")
    def validate_total(cls, value: float, info: ValidationInfo) -> float:
        dishes = info.data.get("jela", [])
        calculated = round(sum(d.cijena for d in dishes), 2)
        if dishes and abs(calculated - value) >= 0.01:
            raise ValueError("Ukupna cijena mora odgovarati zbroju cijena jela.")
        return value


class CCTV_frame(BaseModel):
    id: int
    vrijeme: datetime
    koordinate: Tuple[float, float] = Field(default=(0.0, 0.0))


class BaseCar(BaseModel):
    marka: str
    model: str
    godina_proizvodnje: int = Field(..., gt=1960)
    cijena: float = Field(..., gt=0)
    boja: str


class CarCreate(BaseCar):
    pass


class Car(BaseCar):
    id: int
    cijena_pdv: float = Field(..., gt=0)
