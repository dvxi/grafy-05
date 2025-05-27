# Generator losowej sieci przepływowej i algorytm maksymalnego przepływu

## Opis projektu

Projekt implementuje rozwiązania **Zadania 1** i **Zadania 2** z **Zestawu 5** dotyczącego grafów:

1. **Zadanie 1**: Generator losowej sieci przepływowej
2. **Zadanie 2**: Algorytm Forda-Fulkersona (wersja Edmondsa-Karpa) do znajdowania maksymalnego przepływu

## Zadanie 1: Generator losowej sieci przepływowej

### Procedura generowania sieci

1. **Definiowanie warstw**: 
   - Źródło `s` w warstwie 0
   - `N` warstw pośrednich (1 do N)
   - Ujście `t` w warstwie N+1

2. **Rozmieszczanie wierzchołków**: 
   - W każdej pośredniej warstwie losowo 2-N wierzchołków

3. **Łączenie warstw**: 
   - Zapewnienie spójności od s do t
   - Z każdego wierzchołka wychodzi co najmniej jeden łuk
   - Do każdego wierzchołka wchodzi co najmniej jeden łuk

4. **Dodatkowe łuki**: 
   - Dodanie 2N losowych łuków z ograniczeniami

5. **Przepustowości**: 
   - Przypisanie losowych przepustowości wszystkim krawędziom

## Zadanie 2: Algorytm Forda-Fulkersona (Edmonds-Karp)

### Opis algorytmu

Algorytm znajduje maksymalny przepływ w sieci przepływowej używając:

- **BFS** do znajdowania najkrótszych ścieżek powiększających
- **Sieć rezydualną** do śledzenia dostępnych przepustowości
- **Cofanie przepływu** dla optymalnych rozwiązań

### Kluczowe pojęcia

- **Przepustowość c(u,v)**: Maksymalna ilość jednostek na krawędzi
- **Przepływ f(u,v)**: Faktyczna ilość przepływających jednostek
- **Sieć rezydualna**: Graf z dostępnymi przepustowościami
- **Ścieżka powiększająca**: Ścieżka od s do t w sieci rezydualnej

## Wymagania

- Python 3.7+
- NetworkX
- Matplotlib
- NumPy

## Instalacja

```bash
pip install -r requirements.txt
```

## Użytkowanie

### Zadanie 1: Generator sieci

```bash
python zadanie1_siec_przeplywowa.py
```

### Zadanie 2: Maksymalny przepływ

```bash
python zadanie2_ford_fulkerson.py
```

### Testy algorytmu

```bash
python test_max_flow.py
```

### Użycie w kodzie

```python
from zadanie1_siec_przeplywowa import SiecPrzeplywowa
from zadanie2_ford_fulkerson import FordFulkerson

# Wygeneruj sieć
generator = SiecPrzeplywowa(N=3, min_capacity=1, max_capacity=15)
siec = generator.generuj_siec()

# Znajdź maksymalny przepływ
ford_fulkerson = FordFulkerson(siec)
max_flow = ford_fulkerson.znajdz_maksymalny_przeplyw()

# Wizualizuj wyniki
ford_fulkerson.wizualizuj_wynik(save_file='wynik.png')
```

## Parametry

### Zadanie 1
- `N`: Liczba warstw pośrednich (N ≥ 2)
- `min_capacity`: Minimalna przepustowość krawędzi
- `max_capacity`: Maksymalna przepustowość krawędzi

### Zadanie 2
- `source`: Wierzchołek źródłowy (domyślnie 's')
- `sink`: Wierzchołek ujściowy (domyślnie 't')

## Wyjście

### Zadanie 1
- Szczegółowe informacje o procesie generowania
- Statystyki wygenerowanej sieci
- Wizualizację graficzną sieci z przepustowościami

### Zadanie 2
- Wartość maksymalnego przepływu
- Wizualizację sieci z przepływami w formacie `f(u,v)/c(u,v)`
- Historię iteracji algorytmu
- Statystyki wykorzystania sieci

## Przykłady testowe

Program zawiera kilka przykładów testowych:

1. **Klasyczny przykład** z literatury (Cormen et al.)
2. **Sieci różnych rozmiarów** (N=2,3,4)
3. **Sieć z wąskim gardłem**
4. **Przypadek wymagający cofania przepływu**

## Struktura plików

- `zadanie1_siec_przeplywowa.py` - generator losowej sieci
- `zadanie2_ford_fulkerson.py` - algorytm maksymalnego przepływu
- `test_max_flow.py` - testy algorytmu
- `requirements.txt` - zależności
- `README.md` - dokumentacja
- `*.png` - wygenerowane wizualizacje

## Przykład wyjścia

### Zadanie 1
```
Generator losowej sieci przepływowej
Zadanie 1 - Zestaw 5
========================================
Generuję sieć przepływową z N=3 warstwami pośrednimi...
Utworzone warstwy:
  Warstwa 0: 1 wierzchołków - ['s']
  Warstwa 1: 2 wierzchołków - ['v1_0', 'v1_1']
  Warstwa 2: 3 wierzchołków - ['v2_0', 'v2_1', 'v2_2']
  Warstwa 3: 2 wierzchołków - ['v3_0', 'v3_1']
  Warstwa 4: 1 wierzchołków - ['t']
... 
```

### Zadanie 2
```
Rozpoczynam algorytm Edmondsa-Karpa...
Źródło: s, Ujście: t

--- Iteracja 1 ---
Znaleziona ścieżka: s -> v1_0 -> t
Przepustowość rezydualna ścieżki: 5
...
Maksymalny przepływ: 23
```

## Wizualizacje

Program generuje kolorowe wizualizacje:

- **Zielony**: Źródło (s)
- **Czerwony**: Ujście (t)  
- **Niebieski**: Wierzchołki pośrednie
- **Czerwone krawędzie**: Nasycone
- **Niebieskie krawędzie**: Częściowo wykorzystane
- **Szare krawędzie**: Niewykorzystane

## Autor

Rozwiązanie zadań z kursu Grafy - Zestaw 5, Zadania 1-2 