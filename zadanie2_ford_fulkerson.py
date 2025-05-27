#!/usr/bin/env python3
"""
Zadanie 2 - Algorytm Forda-Fulkersona (wersja Edmondsa-Karpa)
Zestaw 5 - Grafy

Program implementuje algorytm Edmondsa-Karpa do znajdowania maksymalnego przepływu
w sieci przepływowej wygenerowanej w zadaniu 1.

Algorytm używa BFS do znajdowania najkrótszych ścieżek powiększających w sieci rezydualnej.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
from typing import List, Tuple, Dict, Optional, Set
import numpy as np
from zadanie1_siec_przeplywowa import SiecPrzeplywowa


class FordFulkerson:
    def __init__(self, graph: nx.DiGraph):
        """
        Inicjalizuje algorytm Forda-Fulkersona.
        
        Args:
            graph: Graf skierowany z przepustowościami (atrybut 'capacity')
        """
        self.original_graph = graph.copy()
        self.flow = {}  # f(u,v) - przepływ na krawędzi (u,v)
        self.max_flow_value = 0
        self.iterations = []  # Historia iteracji dla wizualizacji
        
        # Inicjalizuj przepływy na 0
        for u, v in self.original_graph.edges():
            self.flow[(u, v)] = 0
    
    def znajdz_maksymalny_przeplyw(self, source: str = 's', sink: str = 't') -> int:
        """
        Znajduje maksymalny przepływ używając algorytmu Edmondsa-Karpa.
        
        Args:
            source: Wierzchołek źródłowy
            sink: Wierzchołek ujściowy
            
        Returns:
            Wartość maksymalnego przepływu
        """
        print(f"Rozpoczynam algorytm Edmondsa-Karpa...")
        print(f"Źródło: {source}, Ujście: {sink}")
        
        iteration = 0
        
        while True:
            iteration += 1
            print(f"\n--- Iteracja {iteration} ---")
            
            # Krok 1: Zbuduj sieć rezydualną
            residual_graph = self._zbuduj_siec_rezydualna()
            
            # Krok 2: Znajdź ścieżkę powiększającą używając BFS
            path, bottleneck = self._znajdz_sciezke_bfs(residual_graph, source, sink)
            
            if path is None:
                print("Brak ścieżki powiększającej - algorytm zakończony")
                break
            
            print(f"Znaleziona ścieżka: {' -> '.join(path)}")
            print(f"Przepustowość rezydualna ścieżki: {bottleneck}")
            
            # Krok 3: Powiększ przepływ wzdłuż ścieżki
            self._powieksz_przeplyw(path, bottleneck)
            
            # Zapisz iterację do historii
            self.iterations.append({
                'iteration': iteration,
                'path': path.copy(),
                'bottleneck': bottleneck,
                'flow': self.flow.copy()
            })
            
            # Oblicz aktualną wartość przepływu
            current_flow = self._oblicz_wartosc_przeplywu(source)
            print(f"Aktualna wartość przepływu: {current_flow}")
        
        self.max_flow_value = self._oblicz_wartosc_przeplywu(source)
        print(f"\nMaksymalny przepływ: {self.max_flow_value}")
        
        return self.max_flow_value
    
    def _zbuduj_siec_rezydualna(self) -> nx.DiGraph:
        """Buduje sieć rezydualną na podstawie aktualnego przepływu."""
        residual = nx.DiGraph()
        
        # Dodaj wszystkie wierzchołki
        residual.add_nodes_from(self.original_graph.nodes())
        
        # Dla każdej krawędzi w oryginalnym grafie
        for u, v in self.original_graph.edges():
            capacity = self.original_graph[u][v]['capacity']
            current_flow = self.flow.get((u, v), 0)
            
            # Krawędź w kierunku oryginalnym (jeśli można jeszcze przesłać)
            residual_capacity = capacity - current_flow
            if residual_capacity > 0:
                residual.add_edge(u, v, capacity=residual_capacity, type='forward')
            
            # Krawędź przeciwna (jeśli można cofnąć przepływ)
            if current_flow > 0:
                residual.add_edge(v, u, capacity=current_flow, type='backward')
        
        return residual
    
    def _znajdz_sciezke_bfs(self, residual_graph: nx.DiGraph, source: str, sink: str) -> Tuple[Optional[List[str]], int]:
        """
        Znajduje najkrótszą ścieżkę powiększającą używając BFS.
        
        Returns:
            Tuple (ścieżka, przepustowość_rezydualna_ścieżki) lub (None, 0)
        """
        if source not in residual_graph or sink not in residual_graph:
            return None, 0
        
        # BFS
        queue = deque([source])
        visited = {source}
        parent = {source: None}
        
        while queue:
            current = queue.popleft()
            
            if current == sink:
                # Znaleziono ścieżkę - rekonstruuj ją
                path = []
                node = sink
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                
                # Oblicz przepustowość rezydualną ścieżki (bottleneck)
                bottleneck = float('inf')
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    edge_capacity = residual_graph[u][v]['capacity']
                    bottleneck = min(bottleneck, edge_capacity)
                
                return path, bottleneck
            
            # Sprawdź wszystkich sąsiadów
            for neighbor in residual_graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return None, 0
    
    def _powieksz_przeplyw(self, path: List[str], bottleneck: int):
        """Powiększa przepływ wzdłuż znalezionej ścieżki."""
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            
            # Sprawdź czy krawędź (u,v) istnieje w oryginalnym grafie
            if self.original_graph.has_edge(u, v):
                # Krawędź w kierunku oryginalnym - zwiększ przepływ
                self.flow[(u, v)] = self.flow.get((u, v), 0) + bottleneck
                print(f"  Zwiększam przepływ {u} -> {v} o {bottleneck}")
            else:
                # Krawędź przeciwna - zmniejsz przepływ na krawędzi (v,u)
                self.flow[(v, u)] = self.flow.get((v, u), 0) - bottleneck
                print(f"  Cofam przepływ {v} -> {u} o {bottleneck}")
    
    def _oblicz_wartosc_przeplywu(self, source: str) -> int:
        """Oblicza wartość przepływu jako sumę przepływów wychodzących ze źródła."""
        total_flow = 0
        for u, v in self.original_graph.edges():
            if u == source:
                total_flow += self.flow.get((u, v), 0)
        return total_flow
    
    def wizualizuj_wynik(self, pozycje: Dict = None, figsize: Tuple[int, int] = (14, 10), 
                        save_file: str = None):
        """Wizualizuje sieć z maksymalnym przepływem."""
        plt.figure(figsize=figsize)
        
        # Jeśli nie podano pozycji, użyj układu spring
        if pozycje is None:
            pozycje = nx.spring_layout(self.original_graph, seed=42)
        
        # Rysuj wierzchołki
        node_colors = []
        for node in self.original_graph.nodes():
            if node == 's':
                node_colors.append('lightgreen')
            elif node == 't':
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightblue')
        
        nx.draw_networkx_nodes(self.original_graph, pozycje,
                              node_color=node_colors,
                              node_size=1000,
                              alpha=0.9)
        
        # Rysuj krawędzie z różnymi kolorami w zależności od nasycenia
        edge_colors = []
        edge_widths = []
        
        for u, v in self.original_graph.edges():
            capacity = self.original_graph[u][v]['capacity']
            flow = self.flow.get((u, v), 0)
            
            # Kolor zależny od nasycenia
            if flow == 0:
                edge_colors.append('lightgray')
                edge_widths.append(1)
            elif flow == capacity:
                edge_colors.append('red')  # Nasycona krawędź
                edge_widths.append(3)
            else:
                edge_colors.append('blue')  # Częściowo wykorzystana
                edge_widths.append(2)
        
        nx.draw_networkx_edges(self.original_graph, pozycje,
                              edge_color=edge_colors,
                              width=edge_widths,
                              arrows=True,
                              arrowsize=20,
                              arrowstyle='->')
        
        # Dodaj etykiety wierzchołków
        nx.draw_networkx_labels(self.original_graph, pozycje, 
                               font_size=12, font_weight='bold')
        
        # Dodaj etykiety krawędzi w formacie f(u,v)/c(u,v)
        edge_labels = {}
        for u, v in self.original_graph.edges():
            capacity = self.original_graph[u][v]['capacity']
            flow = self.flow.get((u, v), 0)
            edge_labels[(u, v)] = f"{flow}/{capacity}"
        
        nx.draw_networkx_edge_labels(self.original_graph, pozycje, edge_labels, 
                                    font_size=9, font_weight='bold')
        
        # Tytuł i legenda
        plt.title(f'Maksymalny przepływ w sieci\n'
                 f'|f_max| = {self.max_flow_value}', 
                 fontsize=16, fontweight='bold')
        
        # Legenda
        legend_elements = [
            patches.Patch(color='lightgreen', label='Źródło (s)'),
            patches.Patch(color='lightcoral', label='Ujście (t)'),
            patches.Patch(color='lightblue', label='Wierzchołki pośrednie'),
            patches.Patch(color='red', label='Krawędzie nasycone'),
            patches.Patch(color='blue', label='Krawędzie częściowo wykorzystane'),
            patches.Patch(color='lightgray', label='Krawędzie niewykorzystane')
        ]
        plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        plt.axis('off')
        plt.tight_layout()
        
        if save_file:
            plt.savefig(save_file, dpi=300, bbox_inches='tight')
            print(f"Wykres zapisano do pliku: {save_file}")
        
        plt.show()
    
    def wypisz_statystyki(self):
        """Wypisuje szczegółowe statystyki przepływu."""
        print("\n" + "="*60)
        print("STATYSTYKI MAKSYMALNEGO PRZEPŁYWU")
        print("="*60)
        
        print(f"Wartość maksymalnego przepływu: {self.max_flow_value}")
        print(f"Liczba iteracji algorytmu: {len(self.iterations)}")
        
        print("\nPrzepływy na krawędziach:")
        total_capacity = 0
        used_capacity = 0
        
        for u, v in self.original_graph.edges():
            capacity = self.original_graph[u][v]['capacity']
            flow = self.flow.get((u, v), 0)
            utilization = (flow / capacity * 100) if capacity > 0 else 0
            
            total_capacity += capacity
            used_capacity += flow
            
            status = ""
            if flow == 0:
                status = " (niewykorzystana)"
            elif flow == capacity:
                status = " (NASYCONA)"
            
            print(f"  {u} -> {v}: {flow}/{capacity} ({utilization:.1f}%){status}")
        
        overall_utilization = (used_capacity / total_capacity * 100) if total_capacity > 0 else 0
        print(f"\nOgólne wykorzystanie sieci: {used_capacity}/{total_capacity} ({overall_utilization:.1f}%)")
        
        # Sprawdź warunek zachowania przepływu
        print("\nSprawdzenie warunku zachowania przepływu:")
        for node in self.original_graph.nodes():
            if node in ['s', 't']:
                continue
            
            inflow = sum(self.flow.get((u, node), 0) for u in self.original_graph.predecessors(node))
            outflow = sum(self.flow.get((node, v), 0) for v in self.original_graph.successors(node))
            
            if inflow == outflow:
                print(f"  {node}: ✓ wpływ={inflow}, wypływ={outflow}")
            else:
                print(f"  {node}: ✗ wpływ={inflow}, wypływ={outflow} (BŁĄD!)")
    
    def wypisz_historie_iteracji(self):
        """Wypisuje historię iteracji algorytmu."""
        print("\n" + "="*60)
        print("HISTORIA ITERACJI ALGORYTMU")
        print("="*60)
        
        for iter_data in self.iterations:
            print(f"\nIteracja {iter_data['iteration']}:")
            print(f"  Ścieżka powiększająca: {' -> '.join(iter_data['path'])}")
            print(f"  Przepustowość rezydualna: {iter_data['bottleneck']}")
            
            # Pokaż zmiany w przepływie
            print("  Zmiany w przepływie:")
            path = iter_data['path']
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if self.original_graph.has_edge(u, v):
                    print(f"    {u} -> {v}: +{iter_data['bottleneck']}")
                else:
                    print(f"    {v} -> {u}: -{iter_data['bottleneck']} (cofanie)")


def demonstracja_algorytmu():
    """Demonstracja działania algorytmu na przykładowej sieci."""
    print("Demonstracja algorytmu Forda-Fulkersona (Edmonds-Karp)")
    print("="*60)
    
    # Wygeneruj przykładową sieć
    print("Generuję przykładową sieć przepływową...")
    generator = SiecPrzeplywowa(N=3, min_capacity=3, max_capacity=12)
    siec = generator.generuj_siec()
    
    print("\nSieć wejściowa:")
    generator.wypisz_statystyki()
    
    # Znajdź maksymalny przepływ
    print("\n" + "="*60)
    ford_fulkerson = FordFulkerson(siec)
    max_flow = ford_fulkerson.znajdz_maksymalny_przeplyw()
    
    # Wypisz wyniki
    ford_fulkerson.wypisz_statystyki()
    ford_fulkerson.wypisz_historie_iteracji()
    
    # Wizualizuj wyniki
    print("\nGeneruję wizualizacje...")
    
    # Użyj pozycji z generatora dla spójności
    pozycje = generator.pozycje
    
    # Wizualizuj oryginalną sieć
    generator.wizualizuj(save_file='siec_oryginalna.png')
    
    # Wizualizuj sieć z maksymalnym przepływem
    ford_fulkerson.wizualizuj_wynik(pozycje=pozycje, save_file='siec_max_flow.png')
    
    return siec, ford_fulkerson


def test_na_prostej_sieci():
    """Test na prostej sieci do weryfikacji poprawności."""
    print("\n" + "="*60)
    print("TEST NA PROSTEJ SIECI")
    print("="*60)
    
    # Utwórz prostą sieć testową
    G = nx.DiGraph()
    G.add_edge('s', 'a', capacity=10)
    G.add_edge('s', 'b', capacity=8)
    G.add_edge('a', 'b', capacity=5)
    G.add_edge('a', 't', capacity=10)
    G.add_edge('b', 't', capacity=10)
    
    print("Sieć testowa:")
    print("s -> a: 10")
    print("s -> b: 8") 
    print("a -> b: 5")
    print("a -> t: 10")
    print("b -> t: 10")
    print("Oczekiwany maksymalny przepływ: 18")
    
    # Znajdź maksymalny przepływ
    ford_fulkerson = FordFulkerson(G)
    max_flow = ford_fulkerson.znajdz_maksymalny_przeplyw()
    
    ford_fulkerson.wypisz_statystyki()
    ford_fulkerson.wypisz_historie_iteracji()
    
    # Wizualizuj
    pozycje = {'s': (0, 0), 'a': (2, 1), 'b': (2, -1), 't': (4, 0)}
    ford_fulkerson.wizualizuj_wynik(pozycje=pozycje, save_file='test_siec_max_flow.png')
    
    return max_flow


def main():
    """Funkcja główna."""
    print("Zadanie 2 - Algorytm Forda-Fulkersona (Edmonds-Karp)")
    print("Zestaw 5 - Grafy")
    print("="*60)
    
    # Test na prostej sieci
    test_flow = test_na_prostej_sieci()
    
    # Demonstracja na losowej sieci
    siec, ford_fulkerson = demonstracja_algorytmu()
    
    print(f"\n" + "="*60)
    print("PODSUMOWANIE")
    print("="*60)
    print(f"Test na prostej sieci - maksymalny przepływ: {test_flow}")
    print(f"Losowa sieć - maksymalny przepływ: {ford_fulkerson.max_flow_value}")
    print("\nWizualizacje zapisano do plików PNG.")


if __name__ == "__main__":
    main() 