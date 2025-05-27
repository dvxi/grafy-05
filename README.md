# Generator losowej sieci przepływowej

## Opis zadania

Program implementuje rozwiązanie **Zadania 1** z **Zestawu 5** dotyczącego grafów. Generuje losową sieć przepływową między pojedynczym źródłem `s` a pojedynczym ujściem `t` zgodnie z określoną procedurą.

## Procedura generowania sieci

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

### Podstawowe uruchomienie

```bash
python zadanie1_siec_przeplywowa.py
```

### Użycie w kodzie

```python
from zadanie1_siec_przeplywowa import SiecPrzeplywowa

# Utwórz generator z N=3 warstwami pośrednimi
generator = SiecPrzeplywowa(N=3, min_capacity=1, max_capacity=15)

# Wygeneruj sieć
siec = generator.generuj_siec()

# Wyświetl statystyki
generator.wypisz_statystyki()

# Wizualizuj sieć
generator.wizualizuj(save_file='moja_siec.png')
```

## Parametry

- `N`: Liczba warstw pośrednich (N ≥ 2)
- `min_capacity`: Minimalna przepustowość krawędzi
- `max_capacity`: Maksymalna przepustowość krawędzi

## Wyjście

Program generuje:
- Szczegółowe informacje o procesie generowania
- Statystyki wygenerowanej sieci
- Wizualizację graficzną sieci z przepustowościami
- Pliki PNG z wykresami

## Przykład wyjścia

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