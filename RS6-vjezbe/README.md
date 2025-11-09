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