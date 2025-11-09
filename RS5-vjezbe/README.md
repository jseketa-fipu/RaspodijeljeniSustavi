
## 2.4 Zadaci za vježbu: Definiranje jednostavnih aiohttp poslužitelja

### Zadatak 1: `GET /proizvodi`

Definirajte `aiohttp` poslužitelj koji radi na portu `8081` koji na putanji `/proizvodi` vraća listu proizvoda u JSON formatu. Svaki proizvod je rječnik koji sadrži ključeve `naziv`, `cijena` i `količina`. Pošaljite zahtjev na adresu `http://localhost:8081/proizvodi` koristeći neki od HTTP klijenata ili `curl` i provjerite odgovor.

### Zadatak 2: `POST /proizvodi`

Nadogradite poslužitelj iz prethodnog zadatka na način da na istoj putanji `/proizvodi` prima POST zahtjeve s podacima o proizvodu. Podaci se šalju u JSON formatu i sadrže ključeve `naziv`, `cijena` i `količina`. _Handler_ funkcija treba ispisati primljene podatke u terminalu, dodati novi proizvod u listu proizvoda i vratiti **odgovor s novom listom proizvoda** u JSON formatu.

### Zadatak 3: `GET /punoljetni`

Definirajte poslužitelj koji sluša na portu `8082` i na putanji `/punoljetni` vraća listu korisnika starijih od 18 godina. Svaki korisnik je rječnik koji sadrži ključeve `ime` i `godine`. Pošaljite zahtjev na adresu `http://localhost:8082/punoljetni` i provjerite odgovor. Novu listu korisnika definirajte koristeći funkciju `filter` ili `list comprehension`.

```python

korisnici = [
  {'ime': 'Ivo', 'godine': 25},
  {'ime': 'Ana', 'godine': 17},
  {'ime': 'Marko', 'godine': 19},
  {'ime': 'Maja', 'godine': 16},
  {'ime': 'Iva', 'godine': 22}
]
```

### Zadatak 4: Dohvaćanje proizvoda

Definirajte `aiohttp` poslužitelj koji radi na portu `8081`. Poslužitelj mora imati dvije rute: `/proizvodi` i `/proizvodi/{id}`. Prva ruta vraća listu proizvoda u JSON formatu, a druga rutu vraća točno jedan proizvod prema ID-u. Ako proizvod s traženim ID-em ne postoji, vratite odgovor s statusom `404` i porukom `{'error': 'Proizvod s traženim ID-em ne postoji'}`.

Proizvode pohranite u listu rječnika:

```python
proizvodi = [
  {"id": 1, "naziv": "Laptop", "cijena": 5000},
  {"id": 2, "naziv": "Miš", "cijena": 100},
  {"id": 3, "naziv": "Tipkovnica", "cijena": 200},
  {"id": 4, "naziv": "Monitor", "cijena": 1000},
  {"id": 5, "naziv": "Slušalice", "cijena": 50}
]
```

Testirajte poslužitelj na sve slučajeve kroz klijentsku sesiju unutar `main` korutine iste skripte.

### Zadatak 5: Proizvodi i ruta za narudžbe

Nadogradite poslužitelj iz prethodnog zadatka na način da podržava i **POST metodu** na putanji `/narudzbe`. Ova ruta prima JSON podatke o novoj narudžbu u sljedećem obliku. Za početak predstavite da je svaka narudžba jednostavna i sadrži samo jedan proizvod i naručenu količinu:

```json
{
  "proizvod_id": 1,
  "kolicina": 2
}
```

_Handler_ korutina ove metode mora provjeriti postoji li proizvod s traženim ID-em unutar liste `proizvodi`. Ako ne postoji, vratite odgovor s statusom `404` i porukom `{'error': 'Proizvod s traženim ID-em ne postoji'}`. Ako proizvod postoji, dodajte novu narudžbu u listu narudžbi i vratite odgovor s nadopunjenom listom narudžbi u JSON formatu i prikladnim statusnim kodom.

Listu narudžbi definirajte globalno, kao praznu listu.

Vaš konačni poslužitelj mora sadržavati 3 rute: `/proizvodi`, `/proizvodi/{id}` i `/narudzbe`.

Testirajte poslužitelj na sve slučajeve kroz klijentsku sesiju unutar `main` korutine iste skripte.

## Zadatak 6: Jednostavna komunikacija

Definirajte 2 mikroservisa u 2 različite datoteke. Prvi mikroservis neka sluša na portu `8081` i na endpointu `/pozdrav` vraća JSON odgovor nakon 3 sekunde čekanja, u formatu: `{"message": "Pozdrav nakon 3 sekunde"}`. Drugi mikroservis neka sluša na portu `8082` te na istom endpointu vraća JSON odgovor nakon 4 sekunde: `{"message": "Pozdrav nakon 4 sekunde"}`.

Unutar `client.py` datoteke definirajte 1 korutinu koja može slati zahtjev na oba mikroservisa, mora primati argumente `url` i `port`. Korutina neka vraća JSON odgovor.

Korutinu pozovite unutar `main` korutine. **Prvo demonstrirajte sekvencijalno slanje zahtjeva, a zatim konkurentno slanje zahtjeva.**

## Zadatak 7: Računske operacije

Definirajte 3 mikroservisa unutar direktorija `microservice_calculations`. Prvi mikroservis neka sluša na portu `8083` i na endpointu `/zbroj` vraća JSON bez čekanja. Ulazni podatak u tijelu zahtjeva neka bude lista brojeva, a odgovor neka bude zbroj svih brojeva. Dodajte provjeru ako brojevi nisu proslijeđeni, vratite odgovarajući HTTP odgovor i statusni kod.

Drugi mikroservis neka sluša na portu `8084` te kao ulazni podataka prima iste podatke. Na endpointu `/umnozak` neka vraća JSON odgovor s umnoškom svih brojeva. Dodajte provjeru ako brojevi nisu proslijeđeni, vratite odgovarajući HTTP odgovor i statusni kod.

Treći mikroservis pozovite nakon konkurentnog izvršavanja prvog i drugog mikroservisa. Dakle treći ide sekvencijalno jer mora čekati rezultati prethodna 2. Ovaj mikroservis neka sluša na portu `8085` te na endpointu `/kolicnik` očekuje JSON s podacima prva dva servisa. Kao odgovor mora vratiti količnik umnoška i zbroja. Dodajte provjeru i vratite odgovarajući statusni kod ako se pokuša umnožak dijeliti s 0.

U `client.py` pozovite konkurentno s proizvoljnim podacima prva dva mikroservisa, a zatim sekvencijalno pozovite treći mikroservis.

## Zadatak 8: Mikroservisna obrada - CatFacts API

Definirajte 2 mikroservisa unutar direktorija `cats`.

Prvi mikroservis `cat_microservice.py` mora slušati na portu `8086` i na endpointu `/cats` vraćati JSON odgovor s listom činjenica o mačkama. Endpoint `/cat` mora primati URL parametar `amount` koji predstavlja broj činjenica koji će se dohvatiti. Na primjer, slanjem zahtjeva na `/cat/30` dohvatit će se 30 činjenica o mačkama. Činjenice se moraju dohvaćati **konkurentnim slanjem zahtjeva na CatFacts API**. Link: https://catfact.ninja/

Drugi mikroservis `cat_fact_check` mora slušati na portu `8087` i na endopintu `/facts` očekivati JSON objekt s listom činjenica o mačkama u tijelu HTTP zahtjeva. Glavna dužnost ovog mikroservisa je da provjeri svaku činjenicu sadrži li riječ `cat` ili `cats`, neovisno o velikim i malim slovima. Odgovor neka bude JSON objekt s novom listom činjenica koje zadovoljavaju prethodni uvjet.

U `client.py` pozovite ove dvije korutine sekvencijalno, obzirom da drugi mikroservis ovisi o rezultatima prvog. Testirajte kod za proizvoljan broj činjenica.
