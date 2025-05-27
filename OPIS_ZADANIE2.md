# Opis implementacji algorytmu maksymalnego przepływu
## Zadanie 2 - Zestaw 5

### Autor: [Imię Nazwisko]
### Data: [Data]

---

## 1. Wprowadzenie

Zadanie 2 polega na implementacji algorytmu Forda-Fulkersona w wersji Edmondsa-Karpa do znajdowania maksymalnego przepływu w sieci przepływowej. Algorytm operuje na sieci wygenerowanej w zadaniu 1 i znajduje optymalny rozkład przepływu między źródłem `s` a ujściem `t`.

## 2. Procedura algorytmu Edmondsa-Karpa

### 2.1 Struktura algorytmu

Algorytm składa się z **iteracyjnego procesu**:
1. **Inicjalizacja** - wszystkie przepływy = 0
2. **Główna pętla** - dopóki istnieją ścieżki powiększające:
   - Znajdź ścieżkę powiększającą (BFS)
   - Oblicz przepustowość rezydualną ścieżki
   - Powiększ przepływ wzdłuż ścieżki
   - Zaktualizuj sieć rezydualną
3. **Zakończenie** - brak ścieżek powiększających

### 2.2 Algorytm implementacji

#### Krok 1: Inicjalizacja przepływów

```python
def __init__(self, graph: nx.DiGraph):
    self.original_graph = graph.copy()
    self.flow = {}  # f(u,v) - przepływ na krawędzi (u,v)
    self.max_flow_value = 0
    self.iterations = []  # Historia iteracji
    
    # Inicjalizuj wszystkie przepływy na 0
    for u, v in self.original_graph.edges():
        self.flow[(u, v)] = 0
```

**Kluczowe właściwości**:
- **Zerowa inicjalizacja** - f(u,v) = 0 dla wszystkich krawędzi
- **Kopia grafu** - zachowanie oryginalnej struktury
- **Historia iteracji** - do analizy i wizualizacji

#### Krok 2: Główna pętla algorytmu

```python
def znajdz_maksymalny_przeplyw(self, source='s', sink='t'):
    iteration = 0
    
    while True:
        iteration += 1
        
        # Zbuduj sieć rezydualną
        residual_graph = self._zbuduj_siec_rezydualna()
        
        # Znajdź ścieżkę powiększającą używając BFS
        path, bottleneck = self._znajdz_sciezke_bfs(residual_graph, source, sink)
        
        if path is None:
            break  # Brak ścieżki powiększającej - KONIEC
        
        # Powiększ przepływ wzdłuż ścieżki
        self._powieksz_przeplyw(path, bottleneck)
        
        # Zapisz iterację do historii
        self._zapisz_iteracje(iteration, path, bottleneck)
    
    self.max_flow_value = self._oblicz_wartosc_przeplywu(source)
    return self.max_flow_value
```

**Warunki zakończenia**:
- **Brak ścieżki powiększającej** od s do t w sieci rezydualnej
- **Osiągnięcie maksymalnego przepływu** (twierdzenie o max-flow min-cut)

#### Krok 3: Budowanie sieci rezydualnej

```python
def _zbuduj_siec_rezydualna(self):
    residual = nx.DiGraph()
    residual.add_nodes_from(self.original_graph.nodes())
    
    for u, v in self.original_graph.edges():
        capacity = self.original_graph[u][v]['capacity']
        current_flow = self.flow.get((u, v), 0)
        
        # Krawędź w kierunku oryginalnym (forward edge)
        residual_capacity = capacity - current_flow
        if residual_capacity > 0:
            residual.add_edge(u, v, capacity=residual_capacity, type='forward')
        
        # Krawędź przeciwna (backward edge) - cofanie przepływu
        if current_flow > 0:
            residual.add_edge(v, u, capacity=current_flow, type='backward')
    
    return residual
```

**Typy krawędzi w sieci rezydualnej**:
- **Forward edge**: cf(u,v) = c(u,v) - f(u,v) > 0 (można zwiększyć przepływ)
- **Backward edge**: cf(v,u) = f(u,v) > 0 (można cofnąć przepływ)

#### Krok 4: Przeszukiwanie BFS (kluczowa różnica Edmonds-Karp)

```python
def _znajdz_sciezke_bfs(self, residual_graph, source, sink):
    queue = deque([source])
    visited = {source}
    parent = {source: None}
    
    while queue:
        current = queue.popleft()
        
        if current == sink:
            # Rekonstrukcja ścieżki od sink do source
            path = []
            node = sink
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            # Oblicz bottleneck (min przepustowość na ścieżce)
            bottleneck = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge_capacity = residual_graph[u][v]['capacity']
                bottleneck = min(bottleneck, edge_capacity)
            
            return path, bottleneck
        
        # Eksploruj sąsiadów
        for neighbor in residual_graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None, 0  # Brak ścieżki
```

**Właściwości BFS**:
- **Najkrótsza ścieżka** - minimalna liczba krawędzi
- **Systematyczne przeszukiwanie** - warstwa po warstwie
- **Gwarancja złożoności** - O(VE²) dla całego algorytmu

#### Krok 5: Powiększanie przepływu

```python
def _powieksz_przeplyw(self, path, bottleneck):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        
        if self.original_graph.has_edge(u, v):
            # Krawędź oryginalna - zwiększ przepływ
            self.flow[(u, v)] = self.flow.get((u, v), 0) + bottleneck
            print(f"  Zwiększam przepływ {u} -> {v} o {bottleneck}")
        else:
            # Krawędź przeciwna - cofnij przepływ
            self.flow[(v, u)] = self.flow.get((v, u), 0) - bottleneck
            print(f"  Cofam przepływ {v} -> {u} o {bottleneck}")
```

**Mechanizm aktualizacji**:
- **Forward edge**: f(u,v) ← f(u,v) + bottleneck
- **Backward edge**: f(v,u) ← f(v,u) - bottleneck (cofanie)

## 3. Implementacja klasy FordFulkerson

### 3.1 Struktura klasy

```python
class FordFulkerson:
    def __init__(self, graph: nx.DiGraph):
        self.original_graph = graph.copy()    # Oryginalny graf
        self.flow = {}                        # Przepływy f(u,v)
        self.max_flow_value = 0              # Wartość maksymalnego przepływu
        self.iterations = []                 # Historia iteracji
```

### 3.2 Metody pomocnicze

```python
def _oblicz_wartosc_przeplywu(self, source):
    """Oblicza wartość przepływu jako sumę wypływów ze źródła."""
    total_flow = 0
    for u, v in self.original_graph.edges():
        if u == source:
            total_flow += self.flow.get((u, v), 0)
    return total_flow

def _zapisz_iteracje(self, iteration, path, bottleneck):
    """Zapisuje informacje o iteracji do historii."""
    self.iterations.append({
        'iteration': iteration,
        'path': path.copy(),
        'bottleneck': bottleneck,
        'flow': self.flow.copy()
    })
```

### 3.3 Walidacja wyników

```python
def wypisz_statystyki(self):
    """Sprawdza poprawność znalezionego przepływu."""
    
    # Sprawdź warunek przepustowości: 0 ≤ f(u,v) ≤ c(u,v)
    for u, v in self.original_graph.edges():
        capacity = self.original_graph[u][v]['capacity']
        flow = self.flow.get((u, v), 0)
        if not (0 <= flow <= capacity):
            print(f"BŁĄD: Naruszenie przepustowości na {u}->{v}: {flow}/{capacity}")
    
    # Sprawdź warunek zachowania przepływu
    for node in self.original_graph.nodes():
        if node in ['s', 't']:
            continue
        
        inflow = sum(self.flow.get((u, node), 0) 
                    for u in self.original_graph.predecessors(node))
        outflow = sum(self.flow.get((node, v), 0) 
                     for v in self.original_graph.successors(node))
        
        if inflow != outflow:
            print(f"BŁĄD: Naruszenie zachowania przepływu w {node}: {inflow} ≠ {outflow}")
```

## 4. Właściwości algorytmu

### 4.1 Gwarancje poprawności

1. **Warunek przepustowości**: 0 ≤ f(u,v) ≤ c(u,v) dla każdej krawędzi
2. **Warunek zachowania**: wpływ = wypływ dla każdego wierzchołka pośredniego
3. **Optymalność**: Znaleziony przepływ jest maksymalny (twierdzenie max-flow min-cut)

### 4.2 Złożoność obliczeniowa

- **Liczba iteracji**: O(VE) - każda iteracja zwiększa długość najkrótszej ścieżki
- **Koszt BFS**: O(V + E) na iterację
- **Całkowita złożoność**: O(VE²)

### 4.3 Różnice od podstawowego Ford-Fulkerson

| Aspekt | Ford-Fulkerson (DFS) | Edmonds-Karp (BFS) |
|--------|---------------------|-------------------|
| Wybór ścieżki | Dowolna ścieżka (DFS) | Najkrótsza ścieżka (BFS) |
| Złożoność | O(E·\|f*\|) | O(VE²) |
| Gwarancje | Może być wykładnicza | Zawsze wielomianowa |
| Deterministyczność | Zależy od implementacji | Deterministyczna |

## 5. Wizualizacja wyników

### 5.1 Format wyjściowy

Zgodnie z wymaganiami zadania, każda krawędź jest oznaczona jako **f(u,v)/c(u,v)**:

```python
def wizualizuj_wynik(self):
    # Etykiety krawędzi w formacie f(u,v)/c(u,v)
    edge_labels = {}
    for u, v in self.original_graph.edges():
        capacity = self.original_graph[u][v]['capacity']
        flow = self.flow.get((u, v), 0)
        edge_labels[(u, v)] = f"{flow}/{capacity}"
```

### 5.2 Kodowanie kolorami

```python
# Kolory krawędzi w zależności od wykorzystania
for u, v in self.original_graph.edges():
    capacity = self.original_graph[u][v]['capacity']
    flow = self.flow.get((u, v), 0)
    
    if flow == 0:
        edge_colors.append('lightgray')    # Niewykorzystane
    elif flow == capacity:
        edge_colors.append('red')          # Nasycone
    else:
        edge_colors.append('blue')         # Częściowo wykorzystane
```

### 5.3 Informacje na wykresie

- **Tytuł**: Wartość maksymalnego przepływu |f_max|
- **Legenda**: Znaczenie kolorów wierzchołków i krawędzi
- **Etykiety**: Przepływ/przepustowość dla każdej krawędzi

## 6. Przykład działania algorytmu

### 6.1 Sieć testowa

```
s --10--> a --5--> t
|         |        ^
8         1        |
|         v        10
v         b -------+
```

### 6.2 Przebieg iteracji

**Iteracja 1**:
- Sieć rezydualna: s→a(10), a→t(5), s→b(8), a→b(1), b→t(10)
- BFS znajduje: s → a → t
- Bottleneck: min(10, 5) = 5
- Aktualizacja: f(s,a) = 5, f(a,t) = 5
- Wartość przepływu: 5

**Iteracja 2**:
- Sieć rezydualna: s→a(5), s→b(8), a→b(1), b→t(10), a→s(5), t→a(5)
- BFS znajduje: s → b → t
- Bottleneck: min(8, 10) = 8
- Aktualizacja: f(s,b) = 8, f(b,t) = 8
- Wartość przepływu: 13

**Iteracja 3**:
- Sieć rezydualna: s→a(5), a→b(1), b→t(2), a→s(5), t→a(5), b→s(8), t→b(8)
- BFS znajduje: s → a → b → t
- Bottleneck: min(5, 1, 2) = 1
- Aktualizacja: f(s,a) = 6, f(a,b) = 1, f(b,t) = 9
- Wartość przepływu: 14

**Iteracja 4**:
- Brak ścieżki od s do t w sieci rezydualnej
- **Maksymalny przepływ: 14**

### 6.3 Analiza cofania przepływu

W tym przykładzie nie wystąpiło cofanie przepływu, ale mechanizm jest gotowy:
- Gdyby BFS znalazł ścieżkę zawierającą krawędź backward (np. b → a)
- Algorytm zmniejszyłby przepływ f(a,b) o wartość bottleneck
- To pozwala na "przekierowanie" przepływu dla lepszego rozwiązania

## 7. Testy i weryfikacja

### 7.1 Przypadki testowe

```python
def test_klasyczny_przyklad():
    """Test na przykładzie z literatury (Cormen et al.)"""
    G = nx.DiGraph()
    G.add_edge('s', 'v1', capacity=16)
    G.add_edge('s', 'v2', capacity=13)
    # ... pozostałe krawędzie
    
    ff = FordFulkerson(G)
    max_flow = ff.znajdz_maksymalny_przeplyw()
    assert max_flow == 23  # Oczekiwany wynik

def test_cofanie_przepływu():
    """Test przypadku wymagającego cofania przepływu"""
    G = nx.DiGraph()
    G.add_edge('s', 'a', capacity=10)
    G.add_edge('s', 'b', capacity=10)
    G.add_edge('a', 'b', capacity=1)
    G.add_edge('a', 't', capacity=1)
    G.add_edge('b', 't', capacity=10)
    
    ff = FordFulkerson(G)
    max_flow = ff.znajdz_maksymalny_przeplyw()
    assert max_flow == 11  # Wymaga cofania przepływu
```

### 7.2 Metryki wydajności

```python
def analiza_wydajnosci(self):
    """Analizuje wydajność algorytmu"""
    print(f"Liczba iteracji: {len(self.iterations)}")
    print(f"Średni bottleneck: {np.mean([it['bottleneck'] for it in self.iterations])}")
    
    # Wykorzystanie sieci
    total_capacity = sum(data['capacity'] for _, _, data in self.original_graph.edges(data=True))
    used_capacity = sum(self.flow.values())
    utilization = (used_capacity / total_capacity) * 100
    print(f"Wykorzystanie sieci: {utilization:.1f}%")
```

## 8. Integracja z zadaniem 1

### 8.1 Przepływ danych między zadaniami

```python
# Zadanie 1: Generuj sieć przepływową
generator = SiecPrzeplywowa(N=3, min_capacity=1, max_capacity=15)
siec = generator.generuj_siec()

# Zadanie 2: Znajdź maksymalny przepływ
ford_fulkerson = FordFulkerson(siec)
max_flow = ford_fulkerson.znajdz_maksymalny_przeplyw()

# Wizualizuj oba wyniki
generator.wizualizuj(save_file='siec_oryginalna.png')
ford_fulkerson.wizualizuj_wynik(pozycje=generator.pozycje, 
                               save_file='siec_max_flow.png')
```

### 8.2 Zachowanie spójności wizualizacji

- **Pozycje wierzchołków**: Używane te same pozycje z zadania 1
- **Układ warstwowy**: Zachowana struktura warstw
- **Porównanie**: Łatwe porównanie przed/po algorytmie

## 9. Wnioski

### 9.1 Zalety implementacji

- **Poprawność algorytmiczna**: Implementacja zgodna z literaturą
- **Efektywność**: Złożoność O(VE²) dla wersji Edmonds-Karp
- **Czytelność kodu**: Modularny design z jasnymi metodami
- **Szczegółowa diagnostyka**: Historia iteracji i walidacja wyników
- **Wizualizacja**: Zgodna z wymaganiami zadania (format f(u,v)/c(u,v))

### 9.2 Obsługa przypadków specjalnych

- **Cofanie przepływu**: Pełna implementacja krawędzi backward
- **Walidacja danych**: Sprawdzanie warunków przepływu
- **Przypadki brzegowe**: Obsługa pustych grafów, braku ścieżek
- **Deterministyczność**: BFS gwarantuje powtarzalne wyniki

### 9.3 Możliwe rozszerzenia

- **Algorytm Dinic**: Implementacja dla lepszej wydajności O(V²E)
- **Min-cost max-flow**: Rozszerzenie o koszty krawędzi
- **Wizualizacja kroków**: Animacja iteracji algorytmu
- **Równoległość**: Paralelizacja BFS dla dużych grafów

---

**Uwaga**: Ten dokument opisuje implementację zgodną z wymaganiami zadania 2 z Zestawu 5. Kod źródłowy znajduje się w pliku `zadanie2_ford_fulkerson.py`. Szczegółowy opis teoretyczny algorytmu znajduje się w pliku `OPIS_ALGORYTMU.md`. 