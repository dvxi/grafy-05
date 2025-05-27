# Opis generatora losowej sieci przepływowej
## Zadanie 1 - Zestaw 5

### Autor: K4
### Data: 27.05.2025

---

## 1. Wprowadzenie

Zadanie 1 polega na implementacji generatora losowej sieci przepływowej zgodnie z określoną procedurą. Generator tworzy sieć między pojedynczym źródłem `s` a pojedynczym ujściem `t` z gwarancją spójności i właściwej struktury warstwowej.

## 2. Procedura generowania sieci

### 2.1 Struktura warstwowa

Sieć jest organizowana w **warstwy**:
- **Warstwa 0**: Źródło `s`
- **Warstwy 1 do N**: Warstwy pośrednie
- **Warstwa N+1**: Ujście `t`

Gdzie `N ≥ 2` to parametr określający liczbę warstw pośrednich.

### 2.2 Algorytm generowania

#### Krok 1: Definiowanie warstw i rozmieszczanie wierzchołków

```python
def _utworz_warstwy(self):
    # Warstwa 0: źródło s
    self.warstwy[0] = ['s']
    
    # Warstwy pośrednie 1 do N
    for i in range(1, self.N + 1):
        liczba_wierzcholkow = random.randint(2, self.N)
        wierzcholki = [f'v{i}_{j}' for j in range(liczba_wierzcholkow)]
        self.warstwy[i] = wierzcholki
    
    # Warstwa N+1: ujście t
    self.warstwy[self.N + 1] = ['t']
```

**Kluczowe właściwości**:
- W każdej warstwie pośredniej jest **losowo od 2 do N wierzchołków**
- Nazewnictwo: `v{warstwa}_{indeks}` dla łatwej identyfikacji
- Deterministyczna struktura warstw z losową zawartością

#### Krok 2: Łączenie wierzchołków między warstwami

```python
def _polacz_warstwy(self):
    for i in range(self.N + 1):
        warstwa_aktualna = self.warstwy[i]
        warstwa_nastepna = self.warstwy[i + 1]
        
        # Z każdego wierzchołka wychodzi co najmniej jeden łuk
        for v in warstwa_aktualna:
            cel = random.choice(warstwa_nastepna)
            self.graph.add_edge(v, cel)
        
        # Do każdego wierzchołka wchodzi co najmniej jeden łuk
        for v in warstwa_nastepna:
            if self.graph.in_degree(v) == 0:
                zrodlo = random.choice(warstwa_aktualna)
                self.graph.add_edge(zrodlo, v)
```

**Gwarancje spójności**:
1. **Z każdego wierzchołka wychodzi ≥ 1 łuk** do następnej warstwy
2. **Do każdego wierzchołka wchodzi ≥ 1 łuk** z poprzedniej warstwy
3. **Istnieje ścieżka od s do t** przez konstrukcję

#### Krok 3: Dodawanie losowych łuków

```python
def _dodaj_losowe_luki(self):
    dodane_luki = 0
    cel_luki = 2 * self.N
    
    while dodane_luki < cel_luki:
        u = random.choice(wszystkie_wierzcholki)
        v = random.choice(wszystkie_wierzcholki)
        
        # Warunki dodania łuku
        if (u != v and 
            not self.graph.has_edge(u, v) and
            v != 's' and 
            u != 't'):
            
            self.graph.add_edge(u, v)
            dodane_luki += 1
```

**Ograniczenia**:
- Dokładnie **2N dodatkowych łuków**
- **Brak łuków wchodzących do źródła** `s`
- **Brak łuków wychodzących z ujścia** `t`
- **Brak duplikatów** krawędzi
- **Brak pętli** (u ≠ v)

#### Krok 4: Przypisanie przepustowości

```python
def _przypisz_przepustowosci(self):
    for u, v in self.graph.edges():
        capacity = random.randint(self.min_capacity, self.max_capacity)
        self.graph[u][v]['capacity'] = capacity
```

**Właściwości przepustowości**:
- **Losowe wartości** z zadanego zakresu [min_capacity, max_capacity]
- **Liczby naturalne** (dodatnie całkowite)
- **Jednolity rozkład** prawdopodobieństwa

## 3. Implementacja klasy SiecPrzeplywowa

### 3.1 Struktura klasy

```python
class SiecPrzeplywowa:
    def __init__(self, N: int, min_capacity: int = 1, max_capacity: int = 10):
        self.N = N                    # Liczba warstw pośrednich
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity
        self.graph = nx.DiGraph()     # Graf NetworkX
        self.warstwy = {}            # Mapowanie warstwa -> wierzchołki
        self.pozycje = {}            # Pozycje do wizualizacji
```

### 3.2 Główna metoda generowania

```python
def generuj_siec(self) -> nx.DiGraph:
    # Krok 1: Definiowanie warstw i rozmieszczanie wierzchołków
    self._utworz_warstwy()
    
    # Krok 2: Łączenie wierzchołków między kolejnymi warstwami
    self._polacz_warstwy()
    
    # Krok 3: Dodawanie 2N dodatkowych losowych łuków
    self._dodaj_losowe_luki()
    
    # Krok 4: Przypisanie przepustowości
    self._przypisz_przepustowosci()
    
    # Oblicz pozycje do wizualizacji
    self._oblicz_pozycje()
    
    return self.graph
```

### 3.3 Pozycjonowanie do wizualizacji

```python
def _oblicz_pozycje(self):
    for warstwa, wierzcholki in self.warstwy.items():
        x = warstwa * 2  # Odstęp między warstwami
        liczba_w = len(wierzcholki)
        
        # Rozmieść równomiernie w pionie
        y_positions = np.linspace(-liczba_w/2, liczba_w/2, liczba_w)
        
        for i, v in enumerate(wierzcholki):
            self.pozycje[v] = (x, y_positions[i])
```

**Układ wizualny**:
- **Warstwy poziomo** - od lewej (s) do prawej (t)
- **Wierzchołki pionowo** - równomiernie rozłożone w każdej warstwie
- **Deterministyczne pozycje** - dla spójnej wizualizacji

## 4. Właściwości wygenerowanej sieci

### 4.1 Gwarancje strukturalne

1. **Spójność**: Zawsze istnieje ścieżka od s do t
2. **Struktura warstwowa**: Wierzchołki zorganizowane w warstwy
3. **Brak cykli wstecznych**: Łuki tylko "do przodu" między warstwami (plus losowe)
4. **Właściwa sieć przepływowa**: Spełnia wszystkie wymagania definicji

### 4.2 Parametry losowości

- **Liczba wierzchołków w warstwie**: 2 do N (losowo)
- **Połączenia między warstwami**: Losowy wybór celów
- **Dodatkowe łuki**: 2N losowych połączeń
- **Przepustowości**: Losowe z zadanego zakresu

### 4.3 Złożoność

- **Wierzchołki**: O(N²) w najgorszym przypadku
- **Krawędzie**: O(N²) + 2N = O(N²)
- **Czas generowania**: O(N²)

## 5. Wizualizacja

### 5.1 Kodowanie kolorami

- **Zielony**: Źródło (s)
- **Czerwony**: Ujście (t)
- **Niebieski**: Wierzchołki pośrednie

### 5.2 Etykiety

- **Wierzchołki**: Nazwy (s, v1_0, v1_1, ..., t)
- **Krawędzie**: Przepustowości (liczby)

### 5.3 Układ

- **Warstwy**: Ułożone od lewej do prawej
- **Wierzchołki**: Równomiernie rozłożone w pionie
- **Strzałki**: Wskazują kierunek przepływu

## 6. Przykład wygenerowanej sieci

Dla N=2, min_capacity=1, max_capacity=5:

```
Warstwa 0: [s]
Warstwa 1: [v1_0, v1_1]  (2 wierzchołki)
Warstwa 2: [v2_0]        (1 wierzchołek)
Warstwa 3: [t]

Krawędzie podstawowe:
s -> v1_0 (capacity: 3)
s -> v1_1 (capacity: 2)
v1_0 -> v2_0 (capacity: 4)
v1_1 -> v2_0 (capacity: 1)
v2_0 -> t (capacity: 5)

Dodatkowe łuki (2*N = 4):
v1_0 -> v1_1 (capacity: 2)
v1_1 -> t (capacity: 3)
s -> v2_0 (capacity: 1)
v1_0 -> t (capacity: 4)
```

## 7. Walidacja poprawności

### 7.1 Sprawdzenia automatyczne

```python
def wypisz_statystyki(self):
    # Sprawdź spójność
    path_exists = nx.has_path(self.graph, 's', 't')
    print(f"Istnieje ścieżka od s do t: {'TAK' if path_exists else 'NIE'}")
    
    # Statystyki strukturalne
    print(f"Liczba wierzchołków: {self.graph.number_of_nodes()}")
    print(f"Liczba krawędzi: {self.graph.number_of_edges()}")
```

### 7.2 Właściwości sieci przepływowej

1. ✅ **Brak krawędzi wchodzących do s**
2. ✅ **Brak krawędzi wychodzących z t**
3. ✅ **Nieujemne przepustowości**
4. ✅ **Spójność od s do t**
5. ✅ **Struktura DAG** (Directed Acyclic Graph) w warstwie podstawowej

## 8. Zastosowanie w zadaniu 2

Wygenerowana sieć służy jako **dane wejściowe** dla algorytmu Forda-Fulkersona:

```python
# Zadanie 1: Generuj sieć
generator = SiecPrzeplywowa(N=3)
siec = generator.generuj_siec()

# Zadanie 2: Znajdź maksymalny przepływ
ford_fulkerson = FordFulkerson(siec)
max_flow = ford_fulkerson.znajdz_maksymalny_przeplyw()
```

## 9. Wnioski

### 9.1 Zalety implementacji

- **Deterministyczna procedura** z kontrolowaną losowością
- **Gwarancja spójności** przez konstrukcję
- **Skalowalna** - parametr N kontroluje rozmiar
- **Wizualizowalna** - czytelny układ warstwowy

### 9.2 Możliwe rozszerzenia

- **Różne rozkłady** liczby wierzchołków w warstwach
- **Ważone prawdopodobieństwa** połączeń
- **Korelacje** między przepustowościami
- **Ograniczenia topologiczne** (np. maksymalny stopień wierzchołka)

---

**Uwaga**: Ten dokument opisuje implementację zgodną z wymaganiami zadania 1 z Zestawu 5. Kod źródłowy znajduje się w pliku `zadanie1_siec_przeplywowa.py`. 
