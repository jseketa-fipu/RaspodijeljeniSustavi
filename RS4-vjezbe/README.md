# 3. Zadaci za vježbu - Slanje konkurentnih HTTP zahtjeva

1. **Definirajte korutinu `fetch_users`** koja će slati GET zahtjev na [JSONPlaceholder API](https://jsonplaceholder.typicode.com/) na URL-u: `https://jsonplaceholder.typicode.com/users`. Morate simulirate slanje 5 zahtjeva konkurentno unutar `main` korutine. Unutar `main` korutine izmjerite vrijeme izvođenja programa, a rezultate pohranite u listu odjedanput koristeći `asyncio.gather` funkciju. Nakon toga koristeći `map` funkcije ili _list comprehension_ izdvojite u zasebne 3 liste: samo imena korisnika, samo email adrese korisnika i samo username korisnika. Na kraju `main` korutine ispišite sve 3 liste i vrijeme izvođenja programa.

<br>

2. **Definirajte dvije korutine**, od kojih će jedna služiti za dohvaćanje činjenica o mačkama koristeći `get_cat_fact` korutinu koja šalje GET zahtjev na URL: `https://catfact.ninja/fact`. Izradite 20 `Task` objekata za dohvaćanje činjenica o mačkama te ih pozovite unutar `main` korutine i rezultate pohranite odjednom koristeći `asyncio.gather` funkciju. Druga korutina `filter_cat_facts` ne šalje HTTP zahtjeve, već mora primiti gotovu listu činjenica o mačkama i vratiti novu listu koja sadrži samo one činjenice koje sadrže riječ "cat" ili "cats" (neovisno o velikim/malim slovima).

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

3. **Definirajte korutinu `get_dog_fact`** koja dohvaća činjenice o psima sa [DOG API](https://dogapi.dog/docs/api-v2).

Korutina `get_dog_fact` neka dohvaća činjenicu o psima na URL-u: `https://dogapi.dog/api/v2/facts`.
Nakon toga, **definirajte korutinu `get_cat_fact`** koja dohvaća činjenicu o mačkama slanjem zahtjeva na URL: `https://catfact.ninja/fact`.

Istovremeno pohranite rezultate izvršavanja ovih _Taskova_ koristeći `asyncio.gather(*dog_facts_tasks, *cat_facts_tasks)` funkciju u listu `dog_cat_facts`, a zatim ih koristeći _list slicing_ odvojite u dvije liste obzirom da znate da je prvih 5 činjenica o psima, a drugih 5 o mačkama.

Na kraju, definirajte i **treću korutinu `mix_facts`** koja prima liste `dog_facts` i `cat_facts` i vraća **novu listu** koja za vrijednost indeksa `i` sadrži činjenicu o psima ako je duljina činjenice o psima veća od duljine činjenice o mačkama na istom indeksu, inače vraća činjenicu o mački. Na kraju ispišite rezultate filtriranog niza činjenica. Liste možete paralelno iterirati koristeći `zip` funkciju, npr. `for dog_fact, cat_fact in zip(dog_facts, cat_facts)`.

_Primjer konačnog ispisa:_

```plaintext
Mixane činjenice o psima i mačkama:

If they have ample water, cats can tolerate temperatures up to 133 °F.
Dogs with little human contact in the first three months typically don’t make good pets.
The most popular dog breed in Canada, U.S., and Great Britain is the Labrador retriever.
An estimated 1,000,000 dogs in the U.S. have been named as the primary beneficiaries in their owner’s will.
When a cats rubs up against you, the cat is marking you with it's scent claiming ownership.
```