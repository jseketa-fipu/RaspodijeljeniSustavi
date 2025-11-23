# 3. Zadaci za vježbu - Konkurentna obrada mrežnih operacija i simulacije grešaka

## Zadatak 1: fetch_users i izdvajanje podataka

**Definirajte korutinu `fetch_users`** koja će slati GET zahtjev na [JSONPlaceholder API](https://jsonplaceholder.typicode.com/) na URL-u: `https://jsonplaceholder.typicode.com/users`. Morate simulirate slanje 5 zahtjeva konkurentno unutar `main` korutine. Unutar `main` korutine izmjerite vrijeme izvođenja programa, a rezultate pohranite u listu odjedanput koristeći `asyncio.gather` funkciju. Nakon toga koristeći `map` funkcije ili _list comprehension_ izdvojite u zasebne 3 liste: samo **imena korisnika**, samo **email adrese korisnika** i samo **username korisnika**. Na kraju `main` korutine ispišite sve 3 liste i vrijeme izvođenja programa.

<br>

## Zadatak 2: filter_cat_facts

**Definirajte dvije korutine**, od kojih će jedna služiti za dohvaćanje činjenica o mačkama koristeći `get_cat_fact` korutinu koja šalje GET zahtjev na URL: `https://catfact.ninja/fact`. Izradite 20 `Task` objekata za dohvaćanje činjenica o mačkama te ih pozovite unutar `main` korutine i rezultate pohranite odjednom koristeći `asyncio.gather` funkciju. Druga korutina `filter_cat_facts` ne šalje HTTP zahtjeve, već zaprima **gotovu listu činjenica (stringova) o mačkama** i vraća novu listu koja sadrži samo one činjenice koje sadrže riječ "cat" ili "cats" (neovisno o velikim/malim slovima).

_Primjer konačnog ispisa:_

```plaintext
Filtrirane činjenice o mačkama:
- A 2007 Gallup poll revealed that both men and women were equally likely to own a cat.
- The first cat in space was a French cat named Felicette (a.k.a. “Astrocat”) In 1963, France blasted the cat into outer space. Electrodes implanted in her brains sent neurological signals back to Earth. She survived the trip.
- The lightest cat on record is a blue point Himalayan called Tinker Toy, who weighed 1 pound, 6 ounces (616 g). Tinker Toy was 2.75 inches (7 cm) tall and 7.5 inches (19 cm) long.
- The first commercially cloned pet was a cat named "Little Nicky." He cost his owner $50,000, making him one of the most expensive cats ever.
- In the 1750s, Europeans introduced cats into the Americas to control pests.
- A group of cats is called a clowder.
```

<br>

<div style="page-break-after: always; break-after: page;"></div>

## Zadatak 3: mix_dog_cat_facts

**Definirajte korutinu `get_dog_fact`** koja dohvaća činjenice o psima sa [DOG API](https://dogapi.dog/docs/api-v2) servisa.

Korutina `get_dog_fact` neka dohvaća činjenicu o psima na URL-u: `https://dogapi.dog/api/v2/facts`.
Nakon toga, **definirajte korutinu `get_cat_fact`** koja dohvaća činjenicu o mačkama slanjem zahtjeva na URL: `https://catfact.ninja/fact`.

Istovremeno pohranite rezultate izvršavanja ovih _Taskova_ koristeći `asyncio.gather(*dog_facts_tasks, *cat_facts_tasks)` funkciju u listu `dog_cat_facts`, a zatim ih koristeći _list slicing_ odvojite u dvije liste obzirom da znate da je prvih 5 činjenica o psima, a drugih 5 o mačkama (bez obzira što mrežni rezultati različito "dolaze", gather ih pohranjuje redoslijedom poziva).

**Na kraju definirajte treću korutinu `mix_facts`** koja prima dvije liste, `dog_facts` i `cat_facts`, te vraća novu listu u kojoj se za svaki indeks `i` nalazi odabrana činjenica prema sljedećem pravilu: uzmite činjenicu o psima ako je njezina duljina veća od duljine odgovarajuće mačje činjenice; u suprotnom odaberite mačju činjenicu. Za paralelnu iteraciju dviju lista upotrijebite funkciju `zip`, npr. `for dog_fact, cat_fact in zip(dog_facts, cat_facts)`. Nakon dobivanja nove liste, ispišite filtrirani skup činjenica.

_Primjer konačnog ispisa:_

```plaintext
Mixane činjenice o psima i mačkama:

If they have ample water, cats can tolerate temperatures up to 133 °F.
Dogs with little human contact in the first three months typically don’t make good pets.
The most popular dog breed in Canada, U.S., and Great Britain is the Labrador retriever.
An estimated 1,000,000 dogs in the U.S. have been named as the primary beneficiaries in their owner’s will.
When a cats rubs up against you, the cat is marking you with it's scent claiming ownership.
```

## Zadatak 4: simulacija autentifikacije korisnika

**Napišite korutinu `autentifikacija` koja simulira proces autentifikacije korisnika**. Korutina treba primiti korisničko ime i lozinku, zatim simulirati sporo I/O čekanje (npr. 2 sekunde) prije nego što vrati `True` ako su korisničko ime i lozinka ispravni. Korisničko ime i lozinku provjerite prema rječniku `korisnici` koji sadrži parove korisničko ime-lozinka.

```python
korisnici = {
    "korisnik1": "lozinka1",
    "korisnik2": "lozinka2",
    "korisnik3": "lozinka3",
}
```

Simulirajte pogrešku u autentifikaciji ako su uneseni podaci netočni (`raise ValueError`).

- Napišite glavnu funkciju koja će poslati konkurentne zahtjeve za autentifikaciju za 5 različitih korisnika (neki s ispravnim, neki s neispravnim podacima). Kako se ponaša `asyncio.gather()` kada se dogodi iznimka u jednoj od korutina?

Izmijenite kod korutine i simulirajte grešku u autentifikaciji koja se javlja **odmah** nakon 3 sekunde čekanja (npr. ne radi autentifikacijski servis) koji će podići iznimku `TimeoutError`.

- Dodajte _timeout_ prilikom **poziva korutine** `autentifikacija` kako biste simulirali situaciju kada autentifikacijski servis ne odgovara na vrijeme.

## Zadatak 5: Pretvorba sinkronog koda u asinkroni

Sljedeći isječak programskog koda pretvorite u asinkroni program s konkurentnom obradom mrežnih zahtjeva:\*\*

```python
import requests

def fetch_url(url: str) -> str:
    response = requests.get(url, timeout=5)
    return response.text

def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://api.github.com"
    ]

    for url in urls:
        content = fetch_url(url)
        print(f"Fetched {len(content)} characters from {url}")

if __name__ == "__main__":
    main()
```

## Zadatak 6: Simulacija raspodijeljenog sustava za dohvaćanje i obradu vremenskih podataka

Radite na raspodijeljenom sustavu za dohvaćanje vremenskih podataka s različitih javnih API-ja\*\*. Vaš servis treba konkurentno agregirati podatke o vremenu iz više izvora te nakon toga izračunati i ispisati prosječnu temperaturu. Definirajte korutinu `fetch_weather_data` (predstavlja mikroservis koji vraća podatke s meteorološke stanice na određenoj lokaciji), koja simulira određeno čekanje (možete staviti nasumično čekanje između 1 i 5 sekundi koristeći `random.uniform(1, 5))` i vraća nasumičnu temperaturu između `20` i `25` stupnjeva Celzijusa. U glavnoj korutini `main` kreirajte i rasporedite 10 objekata tipa Task za konkurentno dohvaćanje vremenskih podataka s 10 različitih vremenskih stanica. Nakon što dobijete sve rezultate, izračunajte i ispišite prosječnu temperaturu.

- Simulirajte situaciju u kojoj nekoliko vremenskih stanica ne odgovara na vrijeme te pravilno obradite iznimku `TimeoutError`.

- Ograničite vrijeme čekanja na svaki zahtjev na najviše 2 sekunde; u suprotnom slučaju vratite `None` te izračunajte prosječnu temperaturu bez podataka za tu mjernu stanicu.

Ako hoćete, možete određene dijelove koda rasporediti u zasebne datoteke (module) ili možete sve napisati u jednoj datoteci.
