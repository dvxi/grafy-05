#!/usr/bin/env python3
"""
Zadanie 1 - Generator losowej sieci przepływowej
Zestaw 5 - Grafy

Program generuje losową sieć przepływową zgodnie z procedurą:
1. Definiuje warstwy od źródła s (warstwa 0) do ujścia t (warstwa N+1)
2. Rozmieszcza losowo 2-N wierzchołków w każdej pośredniej warstwie
3. Łączy wierzchołki między kolejnymi warstwami zapewniając spójność
4. Dodaje 2N dodatkowych losowych łuków
5. Przypisuje przepustowości
6. Wizualizuje sieć
"""

import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Dict, Set
import numpy as np


class SiecPrzeplywowa:
    def __init__(self, N: int, min_capacity: int = 1, max_capacity: int = 10):
        """
        Inicjalizuje generator sieci przepływowej.
        
        Args:
            N: Liczba pośrednich warstw (N >= 2)
            min_capacity: Minimalna przepustowość krawędzi
            max_capacity: Maksymalna przepustowość krawędzi
        """
        if N < 2:
            raise ValueError("N musi być >= 2")
        
        self.N = N
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity
        self.graph = nx.DiGraph()
        self.warstwy = {}  # warstwa -> lista wierzchołków
        self.pozycje = {}  # pozycje wierzchołków do wizualizacji
        
    def generuj_siec(self) -> nx.DiGraph:
        """Generuje losową sieć przepływową zgodnie z procedurą."""
        print(f"Generuję sieć przepływową z N={self.N} warstwami pośrednimi...")
        
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
        
        print(f"Wygenerowano sieć z {self.graph.number_of_nodes()} wierzchołkami "
              f"i {self.graph.number_of_edges()} krawędziami")
        
        return self.graph
    
    def _utworz_warstwy(self):
        """Tworzy warstwy i rozmieszcza wierzchołki."""
        # Warstwa 0: źródło s
        self.warstwy[0] = ['s']
        self.graph.add_node('s', warstwa=0)
        
        # Warstwy pośrednie 1 do N
        for i in range(1, self.N + 1):
            liczba_wierzcholkow = random.randint(2, self.N)
            wierzcholki = [f'v{i}_{j}' for j in range(liczba_wierzcholkow)]
            self.warstwy[i] = wierzcholki
            
            for v in wierzcholki:
                self.graph.add_node(v, warstwa=i)
        
        # Warstwa N+1: ujście t
        self.warstwy[self.N + 1] = ['t']
        self.graph.add_node('t', warstwa=self.N + 1)
        
        print("Utworzone warstwy:")
        for warstwa, wierzcholki in self.warstwy.items():
            print(f"  Warstwa {warstwa}: {len(wierzcholki)} wierzchołków - {wierzcholki}")
    
    def _polacz_warstwy(self):
        """Łączy wierzchołki między kolejnymi warstwami zapewniając spójność."""
        for i in range(self.N + 1):
            warstwa_aktualna = self.warstwy[i]
            warstwa_nastepna = self.warstwy[i + 1]
            
            # Zapewnienie, że z każdego wierzchołka wychodzi co najmniej jeden łuk
            for v in warstwa_aktualna:
                cel = random.choice(warstwa_nastepna)
                self.graph.add_edge(v, cel)
            
            # Zapewnienie, że do każdego wierzchołka wchodzi co najmniej jeden łuk
            for v in warstwa_nastepna:
                if self.graph.in_degree(v) == 0:
                    zrodlo = random.choice(warstwa_aktualna)
                    self.graph.add_edge(zrodlo, v)
        
        print(f"Dodano {self.graph.number_of_edges()} krawędzi podstawowych między warstwami")
    
    def _dodaj_losowe_luki(self):
        """Dodaje 2N dodatkowych losowych łuków."""
        wszystkie_wierzcholki = list(self.graph.nodes())
        dodane_luki = 0
        cel_luki = 2 * self.N
        
        # Maksymalna liczba prób, aby uniknąć nieskończonej pętli
        max_prob = cel_luki * 10
        prob = 0
        
        while dodane_luki < cel_luki and prob < max_prob:
            prob += 1
            
            # Losuj dwa różne wierzchołki
            u = random.choice(wszystkie_wierzcholki)
            v = random.choice(wszystkie_wierzcholki)
            
            # Sprawdź warunki:
            # - różne wierzchołki
            # - łuk nie istnieje
            # - nie dodawaj łuku wchodzącego do s
            # - nie dodawaj łuku wychodzącego z t
            if (u != v and 
                not self.graph.has_edge(u, v) and
                v != 's' and 
                u != 't'):
                
                self.graph.add_edge(u, v)
                dodane_luki += 1
        
        print(f"Dodano {dodane_luki} dodatkowych losowych łuków (cel: {cel_luki})")
    
    def _przypisz_przepustowosci(self):
        """Przypisuje losowe przepustowości wszystkim krawędziom."""
        for u, v in self.graph.edges():
            capacity = random.randint(self.min_capacity, self.max_capacity)
            self.graph[u][v]['capacity'] = capacity
        
        print(f"Przypisano przepustowości z zakresu [{self.min_capacity}, {self.max_capacity}]")
    
    def _oblicz_pozycje(self):
        """Oblicza pozycje wierzchołków do wizualizacji w warstwach."""
        self.pozycje = {}
        
        for warstwa, wierzcholki in self.warstwy.items():
            x = warstwa * 2  # Odstęp między warstwami
            liczba_w = len(wierzcholki)
            
            if liczba_w == 1:
                y_positions = [0]
            else:
                # Rozmieść równomiernie w pionie
                y_positions = np.linspace(-liczba_w/2, liczba_w/2, liczba_w)
            
            for i, v in enumerate(wierzcholki):
                self.pozycje[v] = (x, y_positions[i])
    
    def wizualizuj(self, figsize: Tuple[int, int] = (12, 8), save_file: str = None):
        """Wizualizuje wygenerowaną sieć przepływową."""
        plt.figure(figsize=figsize)
        
        # Rysuj wierzchołki
        node_colors = []
        for node in self.graph.nodes():
            if node == 's':
                node_colors.append('lightgreen')
            elif node == 't':
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightblue')
        
        nx.draw_networkx_nodes(self.graph, self.pozycje, 
                              node_color=node_colors, 
                              node_size=800,
                              alpha=0.9)
        
        # Rysuj krawędzie
        nx.draw_networkx_edges(self.graph, self.pozycje,
                              edge_color='gray',
                              arrows=True,
                              arrowsize=20,
                              arrowstyle='->')
        
        # Dodaj etykiety wierzchołków
        nx.draw_networkx_labels(self.graph, self.pozycje, font_size=10, font_weight='bold')
        
        # Dodaj etykiety przepustowości
        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            edge_labels[(u, v)] = str(data['capacity'])
        
        nx.draw_networkx_edge_labels(self.graph, self.pozycje, edge_labels, font_size=8)
        
        # Dodaj tytuł i legendę
        plt.title(f'Losowa sieć przepływowa (N={self.N})\n'
                 f'Wierzchołki: {self.graph.number_of_nodes()}, '
                 f'Krawędzie: {self.graph.number_of_edges()}', 
                 fontsize=14, fontweight='bold')
        
        # Legenda
        legend_elements = [
            patches.Patch(color='lightgreen', label='Źródło (s)'),
            patches.Patch(color='lightcoral', label='Ujście (t)'),
            patches.Patch(color='lightblue', label='Wierzchołki pośrednie')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.axis('off')
        plt.tight_layout()
        
        if save_file:
            plt.savefig(save_file, dpi=300, bbox_inches='tight')
            print(f"Wykres zapisano do pliku: {save_file}")
        
        plt.show()
    
    def wypisz_statystyki(self):
        """Wypisuje statystyki wygenerowanej sieci."""
        print("\n" + "="*50)
        print("STATYSTYKI SIECI PRZEPŁYWOWEJ")
        print("="*50)
        
        print(f"Liczba warstw pośrednich (N): {self.N}")
        print(f"Całkowita liczba warstw: {self.N + 2}")
        print(f"Liczba wierzchołków: {self.graph.number_of_nodes()}")
        print(f"Liczba krawędzi: {self.graph.number_of_edges()}")
        
        print("\nRozkład wierzchołków w warstwach:")
        for warstwa, wierzcholki in self.warstwy.items():
            if warstwa == 0:
                print(f"  Warstwa {warstwa} (źródło): {len(wierzcholki)} wierzchołków")
            elif warstwa == self.N + 1:
                print(f"  Warstwa {warstwa} (ujście): {len(wierzcholki)} wierzchołków")
            else:
                print(f"  Warstwa {warstwa}: {len(wierzcholki)} wierzchołków")
        
        print(f"\nZakres przepustowości: [{self.min_capacity}, {self.max_capacity}]")
        
        capacities = [data['capacity'] for _, _, data in self.graph.edges(data=True)]
        print(f"Średnia przepustowość: {np.mean(capacities):.2f}")
        print(f"Suma wszystkich przepustowości: {sum(capacities)}")
        
        # Sprawdź spójność
        try:
            path_exists = nx.has_path(self.graph, 's', 't')
            print(f"Istnieje ścieżka od s do t: {'TAK' if path_exists else 'NIE'}")
        except:
            print("Nie można sprawdzić spójności")


def main():
    """Funkcja główna demonstrująca działanie generatora."""
    print("Generator losowej sieci przepływowej")
    print("Zadanie 1 - Zestaw 5")
    print("="*40)
    
    # Parametry
    N = 3  # Liczba warstw pośrednich (można zmienić)
    min_capacity = 1
    max_capacity = 15
    
    # Utwórz generator
    generator = SiecPrzeplywowa(N, min_capacity, max_capacity)
    
    # Wygeneruj sieć
    siec = generator.generuj_siec()
    
    # Wypisz statystyki
    generator.wypisz_statystyki()
    
    # Wizualizuj
    generator.wizualizuj(save_file='siec_przeplywowa.png')
    
    # Opcjonalnie: wygeneruj kilka różnych sieci
    print("\n" + "="*50)
    print("GENEROWANIE DODATKOWYCH PRZYKŁADÓW")
    print("="*50)
    
    for n in [2, 4]:
        print(f"\nGeneruję sieć z N={n}:")
        gen = SiecPrzeplywowa(n, min_capacity, max_capacity)
        gen.generuj_siec()
        gen.wypisz_statystyki()
        gen.wizualizuj(save_file=f'siec_przeplywowa_N{n}.png')


if __name__ == "__main__":
    main() 