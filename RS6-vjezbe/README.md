## How to run (Conda)

1. Create the environment:

```bash
conda env create -f environment.yml
```

2. Activate it:

```bash
conda activate MovieDB
```

3. Run the app:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## 2.2 Zadaci za vježbu - Osnove definicije ruta i Pydantic modela

1. Definirajte novu FastAPI rutu `GET /filmovi` koja će klijentu vraćati listu filmova definiranu u sljedećoj listi:

```python
filmovi = [
  {"id": 1, "naziv": "Titanic", "genre": "drama", "godina": 1997},
  {"id": 2, "naziv": "Inception", "genre": "akcija", "godina": 2010},
  {"id": 3, "naziv": "The Shawshank Redemption", "genre": "drama", "godina": 1994},
  {"id": 4, "naziv": "The Dark Knight", "genre": "akcija", "godina": 2008}
]
```

<br>

2. Nadogradite prethodnu rutu na način da će **output** biti validiran Pydantic modelom `Film` kojeg definirate u zasebnoj datoteci `models.py`.
   <br>
3. Definirajte novu FastAPI rutu `GET /filmovi/{id}` koja će omogućiti pretraživanje novog filma prema `id`-u definiranom u parametru rute `id`. Dodajte i ovdje validaciju Pydantic modelom `Film`.
   <br>
4. Definirajte novu rutu `POST /filmovi` koja će omogućiti dodavanje novog filma u listu filmova. Napravite novi Pydantic model `CreateFilm` koji će sadržavati atribute `naziv`, `genre` i `godina`, a kao output vraćajte validirani Pydantic model `Film` koji predstavlja novododani film s automatski dodijeljenim `id`-em.
   <br>
5. Dodajte query parametre u rutu `GET /filmovi` koji će omogućiti filtriranje filmova prema `genre` i `min_godina`. Zadane vrijednosti za query parametre neka budu `None` i `2000`.

## 2.5 Zadaci za vježbu: Definicija složenijih Pydantic modela

1. Definirajte Pydantic modele `Knjiga` i `Izdavač` koji će validirati podatke i knjigama i izdavačima. Svaka knjiga sastoji se od naslova, imena autora, prezimena autora, godine izdavanja, broja stranica i izdavača. Izdavač se sastoji od naziva i adrese. Ako godina izdavanja nije navedena, zadana vrijednost je trenutna godina.

<br>

2. Definirajte Pydantic model `Admin` koji validira podatke o administratoru sustava. Administrator se sastoji od imena, prezimena, korisničkog imena, emaila te ovlasti. Ovlasti su lista stringova koje mogu sadržavati vrijednosti: `dodavanje`, `brisanje`, `ažuriranje`, `čitanje`. Ako ovlasti nisu navedene, zadana vrijednost je prazna lista. Za ograničavanje ovlasti koristite `Literal` tip iz modula `typing`.

<br>

3. Definirajte Pydantic model `RestaurantOrder` koji se sastoji od informacija o narudžbi u restoranu. Narudžba se sastoji od identifikatora, imena kupca, stol_info, liste jela i ukupne cijene. Definirajte još jedan model za jelo koje se sastoji od identifikatora, naziva i cijene. Za `stol_info` pohranite rječnik koji očekuje ključeve `broj` i `lokacija`. Primjerice, stol_info može biti `{"broj": 5, "lokacija": "terasa"}.` Za definiciju takvog rječnika koristite `TypedDict`tip iz modula`typing`.

<br>

4. Definirajte Pydantic modela `CCTV_frame` koji će validirati podatke o trenutnoj slici s CCTV kamere. Trenutna slika se sastoji od identifikatora, vremena snimanja, te koordiante x i y. Koordinate validirajte kao n-torku decimalnih brojeva. Ako koordinate nisu navedene, zadana vrijednost je `(0.0, 0.0)`.

## 3.2 Zadaci za vježbu: Obrada grešaka

1. Definirajte rutu i odgovarajući Pydantic model za dohvaćanje podataka o automobilima. Svaki automobil ima sljedeće atribute: `id`, `marka`, `model`, `godina_proizvodnje`, `cijena` i `boja`. Ako korisnik pokuša dohvatiti automobil s ID-em koji ne postoji, podignite iznimku `HTTPException` s statusom `404` i porukom `Automobil nije pronađen`.

<br>

2. Nadogradite prethodnu rutu s query parametrima `min_cijena`, `max_cijena`, `min_godina` i `max_godina`. Implementirajte validaciju query parametra za cijenu i godinu proizvodnje. Minimalna cijena mora biti veća od 0, a minimalna godina proizvodnje mora biti veća od 1960. Unutar funkcije obradite iznimku kada korisnik unese minimalnu cijenu veću od maksimalne cijene ili minimalnu godinu proizvodnje veću od maksimalne godine proizvodnje te vratite odgovarajući `HTTPException`.

<br>

3. Definirajte rutu za dodavanje novog automobila u bazu podataka. `id` se mora dodati na poslužitelju, kao i atribut `cijena_pdv` (definirajte dodatni Pydantic model za to). Ako korisnik pokuša dodati automobil koji već postoji u bazi podataka, podignite odgovarajuću iznimku. Implementirajte ukupno 3 Pydantic modela, uključujući `BaseCar` model koji će nasljeđivati preostala 2 modela.





## 4.3 Zadatak za vježbu: Razvoj mikroservisa za dohvaćanje podataka o filmovima

Implementirajte mikroservis za dohvaćanja podataka o filmovima koristeći FastAPI. Mikroservis treba biti organiziran u zasebnim datotekama unutar direktorija `routers` i `models`. Glavni resurs jesu filmovi, a podatke možete preuzeti u JSON obliku sa sljedeće [poveznice](https://gist.github.com/saniyusuf/406b843afdfb9c6a86e25753fe2761f4#file-film-json-L12).

1. Implementirajte odgovarajuće Pydantic modele za filmove prema atributima koji se nalaze u JSON datoteci.
2. Za svaki atribut filma definirajte odgovarajuće polje u Pydantic modelu.
3. Učitajte filmove iz JSON datoteke i [odradite deserijalizaciju podataka](https://www.geeksforgeeks.org/deserialize-json-to-object-in-python/), a zatim ih pohranite u _in-memory_ listu filmova.
4. Dodajte provjere za sljedeće atribute filma unutar Pydantic modela za film:

   - `Images` mora biti lista stringova (javnih poveznica na slike)
   - `type` mora biti odabir između "movie" i "series"
   - Obavezni atributi su: `Title`, `Year`, `Rated`, `Runtime`, `Genre`, `Language`, `Country`, `Actors`, `Plot`, `Writer`
   - Ostali atributi su neobavezni, a ako nisu navedeni, postavite im zadanu vrijednost
   - Dodajte validacije za `Year` i `Runtime` atribut (godina mora biti veća od 1900, a trajanje filma mora biti veće od 0)
   - Dodajte validacije za `imdbRating` i `imdbVotes` (ocjena mora biti između 0 i 10, a broj glasova mora biti veći od 0)

5. Definirajte Pydantic model `Actor` koji će sadržavati atribute `name` i `surname`.
6. Definirajte Pydantic model `Writer` koji će sadržavati atribute `name` i `surname`.
7. Strukturirajte kod u zasebnim datotekma unutar direktorija `routers` i `models`. U direktoriju `routers` dodajte datoteku `filmovi.py` u kojoj ćete definirati rute za dohvaćanje svih filmova i pojedinog filma po `imdbID`-u i rutu za dohvaćanje filma prema naslovu (`Title`).
8. Za rutu koja dohvaća sve filmove, implementirajte mogućnost filtriranja filmova prema query parametrima: `min_year`, `max_year`, `min_rating`, `max_rating` te `type` (film ili serija). Implementirajte validaciju query parametra.
9. U glavnoj aplikaciji učitajte rute iz datoteke `filmovi.py` i uključite ih u glavnu FastAPI aplikaciju.
10. Dodajte iznimke (`HTTPException`) za slučaj kada korisnik pokuša dohvatiti film koji ne postoji u bazi podataka, po `imdbID`-u ili `Title`-u.
11. Testirajte aplikaciju koristeći generiranu interaktivnu dokumentaciju (Swagger ili ReDoc).

Rješenje učitajte na GitHub i predajte na Merlin, uz pripadajuće screenshotove dokumentacije koja se generira automatski na `/docs` ruti.

> Nema univerzalnog rješenja za organizaciju koda i implementaciju API-ja, a zadaća nosi do 2 dodatna boda ovisno o kvaliteti izrade FastAPI mikroservisa.

Swagger docs:
Intro/simple exercises:
<img width="1021" height="1268" alt="image" src="https://github.com/user-attachments/assets/95d829c9-2460-427a-85e2-505f76c0887f" />

<img width="1024" height="1101" alt="image" src="https://github.com/user-attachments/assets/b8b1fa56-fc84-4fb3-99aa-ab7da5486bba" />

<img width="1021" height="999" alt="image" src="https://github.com/user-attachments/assets/ac07f291-d9ed-4afd-aff1-b9a79b021e5e" />

<img width="1018" height="1379" alt="image" src="https://github.com/user-attachments/assets/61488290-dc39-4df7-b69d-0550b284a628" />

<img width="1016" height="1173" alt="image" src="https://github.com/user-attachments/assets/aaf0056a-f60d-45a1-853f-3b3aa1c77380" />

<img width="1022" height="1038" alt="image" src="https://github.com/user-attachments/assets/b87f1aa7-cfcb-4455-8754-8bace3514e72" />

Movies service:
<img width="1031" height="1786" alt="image" src="https://github.com/user-attachments/assets/ec308873-3112-4870-8e61-43c1af9d31a2" />

<img width="1022" height="1305" alt="image" src="https://github.com/user-attachments/assets/7b913f89-36fc-4cde-8e50-2d1cdc3a8a7e" />

<img width="1022" height="1300" alt="image" src="https://github.com/user-attachments/assets/b3527ac1-6add-4fc6-a744-2de5f3e51e9d" />

Schemas:

<img width="1036" height="642" alt="image" src="https://github.com/user-attachments/assets/ccdede9b-04fe-4b88-9a78-2fb5b5cb248f" />










