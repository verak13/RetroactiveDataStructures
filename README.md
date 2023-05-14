## Retroaktivne strukture podataka
Retroaktivne strukture podataka su verzije struktura podataka koje podržavaju modifikacije ne samo u sadašnjosti nego i u prošlosti.
Postoje dva tipa retroaktivnosti:
- *partial retroactivity* - moguće je dodavati, uklanjati ili modifikovati podatke u prošlosti, ali čitati samo u sadašnjosti
- *full retroactivity* - pored modifikacija, moguće je i izvršavati upite nad podacima u prošlosti

Implementirane su tri *partially retroactive* strukture podataka:

### 1. Partially Retroactive Queue

Sadrži listu uvezanih čvorova (*doubly linked list*), pri čemu se čuvaju i podaci o izvršenim operacijama i trenutku u kojem su izvršene. Dodavanje operacija se izvršava u vremenu O(log(n)), jer je potrebno izvršiti binarnu pretragu nad listom operacija da bi se našlo odgovarajuće mjesto za novu operaciju.

Podržane su sljedeće operacije:
- `insert_enqueue(value, time)` - dodavanje operacije enqueue u određenom trenutku. Ako se ne proslijedi time, podrazmijeva se sadašnji trenutak.
- `insert_dequeue(time)` - dodavanje operacije dequeue u određenom trenutku. Ako se ne proslijedi time, podrazmijeva se sadašnji trenutak.
- `delete_operation(time)` - uklanjanje operacije izvršene u određenom trenutku.
- `get_first()` - vraća prvi dodat element koji je na redu za dequeue.
- `get_last()` - vraća posljednji dodat element.

```python
> prq = PartiallyRetroactiveQueue()

> prq.insert_enqueue(value=2, time=10)
Queue = [2] (First=2, Last=2)

> prq.insert_enqueue(value=4, time=20)
Queue = [2, 4] (First=2, Last=4)

> prq.insert_enqueue(value=6, time=30)
Queue = [2, 4, 6] (First=2, Last=6)

> prq.insert_enqueue(value=10)
Queue = [2, 4, 6, 10] (First=2, Last=10)

> prq.insert_dequeue(time=28)
Queue = [4, 6, 10] (First=4, Last=10)

> prq.insert_enqueue(value=8, time=15)
Queue = [8, 4, 6, 10] (First=8, Last=10)

> prq.insert_dequeue(time=16)
Queue = [4, 6, 10] (First=4, Last=10)

> prq.delete_operation(time=40)
Queue = [4, 6] (First=4, Last=6)

> prq.delete_operation(time=28)
Queue = [2, 4, 6] (First=2, Last=6)

> dequeue_operation = prq.insert_dequeue()
First value: 2
Queue = [4, 6] (First=4, Last=6)
```

### 2. Partially Retroactive Stack

Sadrži listu uvezanih čvorova (*doubly linked list*), pri čemu se čuvaju i podaci o izvršenim operacijama i trenutku u kojem su izvršene. Dodavanje operacija se izvršava u vremenu O(log(n)), jer je potrebno izvršiti binarnu pretragu nad listom operacija da bi se našlo odgovarajuće mjesto za novu operaciju.

Podržane su sljedeće operacije:
- `insert_push(value, time)` - dodavanje operacije push u određenom trenutku. Ako se ne proslijedi time, podrazmijeva se sadašnji trenutak.
- `insert_pop(time)` - dodavanje operacije pop u određenom trenutku. Ako se ne proslijedi time, podrazmijeva se sadašnji trenutak. Vraća element koji je posljednji dodat.
- `delete_operation(time)` - uklanjanje operacije izvršene u određenom trenutku.
- `get_top()` - vraća posljednji dodat element.

```python
> prs = PartiallyRetroactiveStack()

> prs.insert_push(value=2, time=10)
Stack = [2] (Top=2)

> prs.insert_push(value=4, time=20)
Stack = [4, 2] (Top=4)

> prs.insert_push(value=6, time=30)
Stack = [6, 4, 2] (Top=6)

> prs.insert_pop(time=28)
Stack = [6, 2] (Top=6)

> prs.insert_push(value=8, time=15)
Stack = [6, 8, 2] (Top=6)

> prs.insert_pop(time=16)
Stack = [6, 2] (Top=6)

> prs.delete_operation(time=30)
Stack = [2] (Top=2)

> prs.delete_operation(time=28)
Stack = [4, 2] (Top=4)

> pop_operation = prs.insert_pop()
Popped value: 4
Stack = [2] (Top=2)
```

### 3. Partially Retroactive Priority Queue

Implementacija se oslanja na *Treap* strukturu podataka (*tree* + *heap*), koja omogućava izvršavanje operacija u vremenu O(log(n)) i pomoću koje su predstavljene sljedeće liste koje su potrebne za implementaciju:
- `queue_now` - svi čvorovi koji se trenutno nalaze u redu sa prioritetom
- `inserts` - svi dodati čvorovi, odnosno trenuci u kojima su dodati čvorovi
- `deleted_inserts` - svi obrisani čvorovi, odnosno trenuci u kojima su obrisani čvorovi
- `bridges` - trenuci u kojima je tadašnji `queue_now` bio podskup sadašnjeg `queue_now`

Podržane su sljedeće operacije:
- `add_insert(time, value, data)` - dodavanje operacije insert u određenom trenutku.
- `add_delete_min(time)` - dodavanje operacije brisanja minimalnog (prvog) elementa u određenom trenutku.
- `remove(time)` - uklanjanje operacije izvršene u određenom trenutku.
- `get_min()` - vraća minimalni (prvi) element u sadašnjem trenutku.

```python
> prpq = PartiallyRetroactivePriorityQueue()

> prpq.add_insert(10, 2, '2')
Min value: (2, '2')
PriorityQueue = [2]

> prpq.add_insert(20, 6, '6')
Min value: (2, '2')
PriorityQueue = [2, 6]

> prpq.add_insert(30, 4, '4')
Min value: (2, '2')
PriorityQueue = [2, 4, 6]

> prpq.add_insert(40, 10, '10')
Min value: (2, '2')
PriorityQueue = [2, 4, 6, 10]

> prpq.add_delete_min(29)
Min value: (4, '4')
PriorityQueue = [4, 6, 10]

> prpq.add_delete_min(28)
Min value: (4, '4')
PriorityQueue = [4, 10]

> prpq.add_insert(15, 1, '1')
Min value: (4, '4')
PriorityQueue = [4, 6, 10]

> prpq.add_insert(16, -1, '-1')
Min value: (2, '2')
PriorityQueue = [2, 4, 6, 10]

> prpq.remove(28)
Min value: (1, '1')
PriorityQueue = [1, 2, 4, 6, 10]

> prpq.remove(30)
Min value: (1, '1')
PriorityQueue = [1, 2, 6, 10]

NOW
|- Node k:2 v:None p:0.029040787574867943 agg:None
|  |- Node k:1 v:None p:0.43788759365057206 agg:None
|  |  |- None
|  |  |- None
|  |- Node k:10 v:None p:0.4453871940548014 agg:None
|  |  |- Node k:6 v:None p:0.9391491627785106 agg:None
|  |  |  |- None
|  |  |  |- None
|  |  |- None

INSERTS
|- Node k:10 v:(2, 10) p:0.22169166627303505 agg:(2, 10)
|  |- None
|  |- Node k:20 v:(6, 20) p:0.38120423768821243 agg:(4, 30)
|  |  |- Node k:15 v:(1, 15) p:0.49581224138185065 agg:(1, 15)
|  |  |  |- None
|  |  |  |- None
|  |  |- Node k:40 v:(10, 40) p:0.7215400323407826 agg:(10, 40)
|  |  |  |- None
|  |  |  |- None

DELETED
|- Node k:16 v:(-1, 16) p:0.21659939713061338 agg:(-1, 16)
|  |- None
|  |- None

BRIDGES
|- Node k:40 v:Ag(sum:0 min_key:40 max_key:40)  p:0.0021060533511106927 agg:Ag(sum:1 min_key:10 max_key:40) 
|  |- Node k:29 v:Ag(sum:-1 min_key:29 max_key:29)  p:0.22876222127045265 agg:Ag(sum:1 min_key:10 max_key:29) 
|  |  |- Node k:16 v:Ag(sum:1 min_key:16 max_key:16)  p:0.4221165755827173 agg:Ag(sum:2 min_key:10 max_key:28) 
|  |  |  |- Node k:15 v:Ag(sum:0 min_key:15 max_key:15)  p:0.5414124727934966 agg:Ag(sum:2 min_key:10 max_key:15) 
|  |  |  |  |- Node k:10 v:Ag(sum:0 min_key:10 max_key:10)  p:0.8474337369372327 agg:Ag(sum:1 min_key:10 max_key:10) 
|  |  |  |  |  |- None
|  |  |  |  |  |- None
|  |  |  |  |- None
|  |  |  |- Node k:20 v:Ag(sum:0 min_key:20 max_key:20)  p:0.4494910647887381 agg:Ag(sum:-1 min_key:20 max_key:28) 
|  |  |  |  |- None
|  |  |  |  |- None
|  |  |- None
|  |- None
```

### Primjena
U fajlu *dijkstra.py* dat je primjer primjene parcijalno retroaktivnog reda sa prioritetom u *dijkstra* algoritmu za traženje najkraćih rastojanja od određeng čvora u grafu.

```python
    > prpq = PartiallyRetroactivePriorityQueue()

    > example_graph = {
        'E': {'F': 20, 'D': 50, 'A': 10},
        'F': {'E': 20, 'A': 20, 'D': 30},
        'D': {'F': 30, 'E': 50, 'A': 30, 'B': 10, 'C': 50},
        'A': {'E': 10, 'F': 20, 'D': 30, 'B': 10},
        'B': {'A': 10, 'D': 10, 'C': 10},
        'C': {'D': 50, 'B': 10},
    }

    > distances = calculate_distances_prpq(prpq, example_graph, 'A')
    > print(distances)
    {'E': 10, 'F': 20, 'D': 20, 'A': 0, 'B': 10, 'C': 20}
```

### Literatura

- https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/pages/calendar-and-notes/

- [Retroactive Data Structures, Erik D. Demaine, John Ianoco, Stefan Langerman](https://erikdemaine.org/papers/Retroactive_TALG/paper.pdf)

- [Fully Retroactive Priority Queues, Erik D. Demaine](https://adamyedidia.files.wordpress.com/2014/11/revised_paper.pdf)

- https://github.com/6851-2021/retroactive-priority-queue

