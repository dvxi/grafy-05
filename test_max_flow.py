#!/usr/bin/env python3
"""
Skrypt testowy dla algorytmu maksymalnego przepływu
Pozwala na łatwe testowanie różnych konfiguracji sieci
"""

from zadanie1_siec_przeplywowa import SiecPrzeplywowa
from zadanie2_ford_fulkerson import FordFulkerson
import networkx as nx


def test_klasyczny_przyklad():
    """Test na klasycznym przykładzie z literatury."""
    print("="*50)
    print("TEST: Klasyczny przykład z literatury")
    print("="*50)
    
    # Sieć z przykładu Cormen et al.
    G = nx.DiGraph()
    G.add_edge('s', 'v1', capacity=16)
    G.add_edge('s', 'v2', capacity=13)
    G.add_edge('v1', 'v2', capacity=10)
    G.add_edge('v1', 'v3', capacity=12)
    G.add_edge('v2', 'v1', capacity=4)
    G.add_edge('v2', 'v4', capacity=14)
    G.add_edge('v3', 'v2', capacity=9)
    G.add_edge('v3', 't', capacity=20)
    G.add_edge('v4', 'v3', capacity=7)
    G.add_edge('v4', 't', capacity=4)
    
    print("Struktura sieci:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} -> {v}: {data['capacity']}")
    
    print("\nOczekiwany maksymalny przepływ: 23")
    
    # Znajdź maksymalny przepływ
    ff = FordFulkerson(G)
    max_flow = ff.znajdz_maksymalny_przeplyw()
    
    ff.wypisz_statystyki()
    
    # Wizualizuj
    pozycje = {
        's': (0, 0),
        'v1': (2, 1),
        'v2': (2, -1),
        'v3': (4, 1),
        'v4': (4, -1),
        't': (6, 0)
    }
    ff.wizualizuj_wynik(pozycje=pozycje, save_file='klasyczny_przyklad.png')
    
    return max_flow


def test_rozne_rozmiary():
    """Test na sieciach różnych rozmiarów."""
    print("\n" + "="*50)
    print("TEST: Sieci różnych rozmiarów")
    print("="*50)
    
    wyniki = {}
    
    for N in [2, 3, 4]:
        print(f"\n--- Test dla N={N} ---")
        
        # Wygeneruj sieć
        generator = SiecPrzeplywowa(N=N, min_capacity=1, max_capacity=10)
        siec = generator.generuj_siec()
        
        # Znajdź maksymalny przepływ
        ff = FordFulkerson(siec)
        max_flow = ff.znajdz_maksymalny_przeplyw()
        
        wyniki[N] = {
            'max_flow': max_flow,
            'nodes': siec.number_of_nodes(),
            'edges': siec.number_of_edges(),
            'iterations': len(ff.iterations)
        }
        
        print(f"Wyniki dla N={N}:")
        print(f"  Wierzchołki: {wyniki[N]['nodes']}")
        print(f"  Krawędzie: {wyniki[N]['edges']}")
        print(f"  Maksymalny przepływ: {wyniki[N]['max_flow']}")
        print(f"  Iteracje algorytmu: {wyniki[N]['iterations']}")
        
        # Zapisz wizualizację
        ff.wizualizuj_wynik(pozycje=generator.pozycje, 
                           save_file=f'test_N{N}_max_flow.png')
    
    return wyniki


def test_wąskie_gardło():
    """Test sieci z wąskim gardłem."""
    print("\n" + "="*50)
    print("TEST: Sieć z wąskim gardłem")
    print("="*50)
    
    # Sieć gdzie jedno miejsce ogranicza cały przepływ
    G = nx.DiGraph()
    G.add_edge('s', 'a', capacity=100)
    G.add_edge('s', 'b', capacity=100)
    G.add_edge('a', 'c', capacity=1)  # Wąskie gardło
    G.add_edge('b', 'c', capacity=100)
    G.add_edge('c', 't', capacity=100)
    
    print("Sieć z wąskim gardłem (a->c: 1):")
    for u, v, data in G.edges(data=True):
        print(f"  {u} -> {v}: {data['capacity']}")
    
    print("Oczekiwany maksymalny przepływ: 101")
    
    ff = FordFulkerson(G)
    max_flow = ff.znajdz_maksymalny_przeplyw()
    
    ff.wypisz_statystyki()
    
    pozycje = {
        's': (0, 0),
        'a': (2, 1),
        'b': (2, -1),
        'c': (4, 0),
        't': (6, 0)
    }
    ff.wizualizuj_wynik(pozycje=pozycje, save_file='waskie_gardlo.png')
    
    return max_flow


def test_cofanie_przepływu():
    """Test przypadku wymagającego cofania przepływu."""
    print("\n" + "="*50)
    print("TEST: Przypadek z cofaniem przepływu")
    print("="*50)
    
    # Sieć gdzie cofanie przepływu jest konieczne dla optymalnego rozwiązania
    G = nx.DiGraph()
    G.add_edge('s', 'a', capacity=10)
    G.add_edge('s', 'b', capacity=10)
    G.add_edge('a', 'b', capacity=1)
    G.add_edge('a', 't', capacity=1)
    G.add_edge('b', 't', capacity=10)
    
    print("Sieć wymagająca cofania przepływu:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} -> {v}: {data['capacity']}")
    
    print("Oczekiwany maksymalny przepływ: 11")
    print("(Wymaga cofania przepływu w co najmniej jednej iteracji)")
    
    ff = FordFulkerson(G)
    max_flow = ff.znajdz_maksymalny_przeplyw()
    
    ff.wypisz_statystyki()
    ff.wypisz_historie_iteracji()
    
    pozycje = {
        's': (0, 0),
        'a': (2, 1),
        'b': (2, -1),
        't': (4, 0)
    }
    ff.wizualizuj_wynik(pozycje=pozycje, save_file='cofanie_przepływu.png')
    
    return max_flow


def main():
    """Uruchamia wszystkie testy."""
    print("TESTY ALGORYTMU MAKSYMALNEGO PRZEPŁYWU")
    print("Zadanie 2 - Zestaw 5")
    print("="*60)
    
    # Uruchom wszystkie testy
    wyniki = {}
    
    wyniki['klasyczny'] = test_klasyczny_przyklad()
    wyniki['rozmiary'] = test_rozne_rozmiary()
    wyniki['waskie_gardlo'] = test_wąskie_gardło()
    wyniki['cofanie'] = test_cofanie_przepływu()
    
    # Podsumowanie
    print("\n" + "="*60)
    print("PODSUMOWANIE TESTÓW")
    print("="*60)
    
    print(f"Klasyczny przykład: {wyniki['klasyczny']} (oczekiwane: 23)")
    print(f"Wąskie gardło: {wyniki['waskie_gardlo']} (oczekiwane: 101)")
    print(f"Cofanie przepływu: {wyniki['cofanie']} (oczekiwane: 11)")
    
    print("\nTesty różnych rozmiarów:")
    for N, dane in wyniki['rozmiary'].items():
        print(f"  N={N}: przepływ={dane['max_flow']}, "
              f"wierzchołki={dane['nodes']}, "
              f"krawędzie={dane['edges']}, "
              f"iteracje={dane['iterations']}")
    
    print("\nWszystkie wizualizacje zapisano do plików PNG.")


if __name__ == "__main__":
    main() 