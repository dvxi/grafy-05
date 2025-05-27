# Opis działania algorytmu Forda-Fulkersona (Edmonds-Karp)
## Zadanie 2 - Zestaw 5

### Autor: [Imię Nazwisko]
### Data: [Data]

---

## 1. Wprowadzenie

Niniejszy dokument opisuje implementację algorytmu Forda-Fulkersona w wersji Edmondsa-Karpa do znajdowania maksymalnego przepływu w sieci przepływowej. Algorytm został zaimplementowany zgodnie z wymaganiami zadania 2 z Zestawu 5.

## 2. Teoretyczne podstawy algorytmu

### 2.1 Definicje podstawowe

**Sieć przepływowa** to digraf G = (V, E) z funkcją przepustowości c: E → ℝ⁺ oraz wyróżnionymi wierzchołkami:
- **Źródło s** - wierzchołek bez krawędzi wchodzących
- **Ujście t** - wierzchołek bez krawędzi wychodzących

**Przepływ** f to funkcja f: E → ℝ spełniająca:
1. **Warunek przepustowości**: 0 ≤ f(u,v) ≤ c(u,v) dla każdej krawędzi (u,v)
2. **Warunek zachowania przepływu**: ∑ᵤ f(u,v) = ∑ᵤ f(v,u) dla każdego v ∉ {s,t}

**Wartość przepływu**: |f| = ∑ᵥ f(s,v) = ∑ᵥ f(v,t)

### 2.2 Sieć rezydualna

**Sieć rezydualna** Gf = (V, Ef) zawiera krawędzie z dodatnią **przepustowością rezydualną**:

- Dla krawędzi (u,v) ∈ E: cf(u,v) = c(u,v) - f(u,v)
- Dla krawędzi przeciwnej: cf(v,u) = f(u,v)

**Ścieżka powiększająca** to ścieżka od s do t w Gf.

## 3. Algorytm Edmondsa-Karpa

### 3.1 Pseudokod

```
EDMONDS-KARP(G, s, t):
1. for każda krawędź (u,v) ∈ E:
2.     f(u,v) = 0
3. while istnieje ścieżka p od s do t w Gf:
4.     cf(p) = min{cf(u,v) : (u,v) ∈ p}
5.     for każda krawędź (u,v) ∈ p:
6.         if (u,v) ∈ E:
7.             f(u,v) = f(u,v) + cf(p)
8.         else:
9.             f(v,u) = f(v,u) - cf(p)
10. return |f|
```

### 3.2 Kluczowe różnice od podstawowego Ford-Fulkerson

- **BFS zamiast DFS**: Edmonds-Karp używa BFS do znajdowania najkrótszych ścieżek
- **Złożoność**: O(VE²) zamiast potencjalnie wykładniczej
- **Deterministyczność**: Zawsze znajduje ścieżkę o najmniejszej liczbie krawędzi

## 4. Implementacja

### 4.1 Struktura klasy FordFulkerson

```python
class FordFulkerson:
    def __init__(self, graph: nx.DiGraph):
        self.original_graph = graph.copy()
        self.flow = {}  # Przepływy f(u,v)
        self.max_flow_value = 0
        self.iterations = []  # Historia dla analizy
```

### 4.2 Główna pętla algorytmu

```python
def znajdz_maksymalny_przeplyw(self, source='s', sink='t'):
    iteration = 0
    while True:
        iteration += 1
        
        # Krok 1: Zbuduj sieć rezydualną
        residual_graph = self._zbuduj_siec_rezydualna()
        
        # Krok 2: Znajdź ścieżkę BFS
        path, bottleneck = self._znajdz_sciezke_bfs(residual_graph, source, sink)
        
        if path is None:
            break  # Brak ścieżki powiększającej
            
        # Krok 3: Powiększ przepływ
        self._powieksz_przeplyw(path, bottleneck)
```

### 4.3 Budowanie sieci rezydualnej

Dla każdej krawędzi (u,v) w oryginalnym grafie:

```python
def _zbuduj_siec_rezydualna(self):
    residual = nx.DiGraph()
    residual.add_nodes_from(self.original_graph.nodes())
    
    for u, v in self.original_graph.edges():
        capacity = self.original_graph[u][v]['capacity']
        current_flow = self.flow.get((u, v), 0)
        
        # Krawędź w kierunku oryginalnym
        residual_capacity = capacity - current_flow
        if residual_capacity > 0:
            residual.add_edge(u, v, capacity=residual_capacity, type='forward')
        
        # Krawędź przeciwna (cofanie przepływu)
        if current_flow > 0:
            residual.add_edge(v, u, capacity=current_flow, type='backward')
```

**Kluczowe aspekty**:
- Krawędzie "forward" pozwalają na zwiększenie przepływu
- Krawędzie "backward" pozwalają na cofanie przepływu
- Tylko krawędzie z cf(u,v) > 0 są dodawane do sieci rezydualnej

### 4.4 Przeszukiwanie BFS

```python
def _znajdz_sciezke_bfs(self, residual_graph, source, sink):
    queue = deque([source])
    visited = {source}
    parent = {source: None}
    
    while queue:
        current = queue.popleft()
        
        if current == sink:
            # Rekonstrukcja ścieżki
            path = []
            node = sink
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            # Oblicz bottleneck
            bottleneck = min(residual_graph[u][v]['capacity'] 
                           for u, v in zip(path[:-1], path[1:]))
            
            return path, bottleneck
```

**Właściwości BFS**:
- Znajduje ścieżkę o najmniejszej liczbie krawędzi
- Gwarantuje złożoność O(VE²)
- Systematyczne przeszukiwanie "warstwami"

### 4.5 Powiększanie przepływu

```python
def _powieksz_przeplyw(self, path, bottleneck):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        
        if self.original_graph.has_edge(u, v):
            # Krawędź oryginalna - zwiększ przepływ
            self.flow[(u, v)] += bottleneck
        else:
            # Krawędź przeciwna - cofnij przepływ
            self.flow[(v, u)] -= bottleneck
```

**Mechanizm cofania przepływu**:
- Jeśli ścieżka zawiera krawędź (u,v) nie będącą w oryginalnym grafie
- To odpowiada krawędzi (v,u) w oryginalnym grafie
- Zmniejszamy przepływ f(v,u) o wartość bottleneck

## 5. Przykład działania algorytmu

### 5.1 Sieć testowa

Rozważmy prostą sieć:
```
s --10--> a --1--> t
|         ^        ^
8         |        |
|         1        10
v         |        |
b --------+--------+
```

### 5.2 Przebieg algorytmu

**Iteracja 1**:
- Ścieżka BFS: s → a → t
- Bottleneck: min(10, 1) = 1
- Przepływ: f(s,a) = 1, f(a,t) = 1
- Wartość przepływu: 1

**Iteracja 2**:
- Ścieżka BFS: s → b → t
- Bottleneck: min(8, 10) = 8
- Przepływ: f(s,b) = 8, f(b,t) = 8
- Wartość przepływu: 9

**Iteracja 3**:
- Ścieżka BFS: s → a → b → t (używa krawędzi a→b)
- Bottleneck: min(9, 1, 2) = 1
- Przepływ: f(s,a) = 2, f(a,b) = 1, f(b,t) = 9
- Wartość przepływu: 10

**Iteracja 4**:
- Ścieżka BFS: s → b → a → t (cofanie przez a→b)
- Bottleneck: min(6, 1, 0) = 0
- Brak ścieżki powiększającej - KONIEC

**Maksymalny przepływ**: 10

### 5.3 Znaczenie cofania przepływu

W iteracji 4 algorytm próbuje użyć krawędzi b → a, która jest krawędzią przeciwną do a → b. To pozwala na "przekierowanie" części przepływu i potencjalne znalezienie lepszego rozwiązania.

## 6. Złożoność obliczeniowa

### 6.1 Analiza teoretyczna

- **Liczba iteracji**: O(VE) - każda iteracja zwiększa odległość najkrótszej ścieżki
- **Koszt BFS**: O(V + E) na iterację
- **Całkowita złożoność**: O(VE²)

### 6.2 Porównanie z innymi wariantami

| Wariant | Złożoność | Uwagi |
|---------|-----------|-------|
| Ford-Fulkerson (DFS) | O(E·|f*|) | Może być wykładnicza |
| Edmonds-Karp (BFS) | O(VE²) | Zawsze wielomianowa |
| Dinic | O(V²E) | Szybszy dla gęstych grafów |
| Push-Relabel | O(V³) | Najszybszy dla wielu przypadków |

## 7. Implementacyjne szczegóły

### 7.1 Reprezentacja grafu

- **NetworkX DiGraph**: Wygodne API, bogate funkcjonalności
- **Atrybuty krawędzi**: `capacity` dla przepustowości
- **Słownik przepływów**: `self.flow[(u,v)]` dla każdej krawędzi

### 7.2 Obsługa przypadków brzegowych

```python
# Sprawdzenie istnienia wierzchołków
if source not in residual_graph or sink not in residual_graph:
    return None, 0

# Inicjalizacja przepływów
for u, v in self.original_graph.edges():
    self.flow[(u, v)] = 0

# Bezpieczne pobieranie przepływu
current_flow = self.flow.get((u, v), 0)
```

### 7.3 Walidacja wyników

Program sprawdza:
1. **Warunek przepustowości**: 0 ≤ f(u,v) ≤ c(u,v)
2. **Warunek zachowania**: wpływ = wypływ dla każdego wierzchołka pośredniego
3. **Spójność**: wartość przepływu = suma wypływów ze źródła

## 8. Wizualizacja wyników

### 8.1 Format etykiet krawędzi

Każda krawędź jest oznaczona jako `f(u,v)/c(u,v)`, gdzie:
- f(u,v) - aktualny przepływ
- c(u,v) - przepustowość

### 8.2 Kodowanie kolorami

- **Czerwone krawędzie**: Nasycone (f(u,v) = c(u,v))
- **Niebieskie krawędzie**: Częściowo wykorzystane (0 < f(u,v) < c(u,v))
- **Szare krawędzie**: Niewykorzystane (f(u,v) = 0)

### 8.3 Wierzchołki

- **Zielony**: Źródło (s)
- **Czerwony**: Ujście (t)
- **Niebieski**: Wierzchołki pośrednie

## 9. Testy i weryfikacja

### 9.1 Przypadki testowe

1. **Klasyczny przykład** (Cormen et al.): Weryfikacja na znanym przykładzie
2. **Wąskie gardło**: Test identyfikacji ograniczających krawędzi
3. **Cofanie przepływu**: Przypadek wymagający backtracking
4. **Różne rozmiary**: Skalowalność algorytmu

### 9.2 Metryki wydajności

- Liczba iteracji algorytmu
- Wykorzystanie przepustowości sieci
- Czas wykonania (dla większych sieci)

## 10. Wnioski

### 10.1 Zalety implementacji

- **Poprawność**: Algorytm zawsze znajduje optymalny przepływ
- **Efektywność**: Złożoność O(VE²) jest akceptowalna
- **Czytelność**: Kod jest dobrze udokumentowany i modularny
- **Wizualizacja**: Wyniki są łatwe do interpretacji

### 10.2 Możliwe rozszerzenia

- Implementacja algorytmu Dinic dla lepszej wydajności
- Obsługa sieci z kosztami (min-cost max-flow)
- Równoległe przetwarzanie dla bardzo dużych sieci
- Interaktywna wizualizacja kroków algorytmu

### 10.3 Zastosowania praktyczne

- Sieci transportowe i logistyczne
- Przepływ danych w sieciach komputerowych
- Planowanie zasobów w systemach produkcyjnych
- Analiza przepustowości w sieciach społecznych

---

## Bibliografia

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
2. Edmonds, J., & Karp, R. M. (1972). Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM*, 19(2), 248-264.
3. Ford, L. R., & Fulkerson, D. R. (1956). Maximal flow through a network. *Canadian Journal of Mathematics*, 8, 399-404.

---

**Uwaga**: Ten dokument opisuje implementację zgodną z wymaganiami zadania 2 z Zestawu 5. Kod źródłowy znajduje się w pliku `zadanie2_ford_fulkerson.py`. 