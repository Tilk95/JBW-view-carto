"""
Module de gestion des données CSV pour JBW Viewer
================================================

Ce module gère la lecture et le traitement du fichier CSV contenant
les Points de Référence (PR) avec leurs coordonnées Lambert 93.

Auteur: Assistant IA
Date: 2025
Version: 1.0
"""

import csv
import os
from typing import List, Dict, Tuple


class DataManager:
    """
    Gestionnaire de données pour les Points de Référence (PR).
    
    Cette classe s'occupe de :
    - Charger le fichier CSV des PR
    - Nettoyer et valider les données
    - Fournir les données formatées pour la cartographie
    """
    
    def __init__(self, csv_file_path: str = "data/TTH_EXPLORER_REFERENTIEL_PR.csv"):
        """
        Initialise le gestionnaire de données.
        
        Args:
            csv_file_path (str): Chemin vers le fichier CSV des PR
        """
        self.csv_file_path = csv_file_path
        self.pr_data = []
        self.load_data()
    
    def load_data(self) -> bool:
        """
        Charge et nettoie les données du fichier CSV.
        
        Le fichier CSV contient les colonnes :
        - codeCI : Code d'identification CI
        - codeCH : Code d'identification CH  
        - libelleCI : Libellé descriptif
        - XLambert93 : Coordonnée X en Lambert 93
        - YLambert93 : Coordonnée Y en Lambert 93
        """
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Nettoyer les données (supprimer espaces et guillemets)
                    cleaned_row = {
                        'codeCI': row['codeCI'].strip().strip('"'),
                        'codeCH': row['codeCH'].strip().strip('"'),
                        'libelleCI': row['libelleCI'].strip().strip('"'),
                        'XLambert93': float(row['XLambert93'].strip().strip('"').replace(',', '.')),
                        'YLambert93': float(row['YLambert93'].strip().strip('"').replace(',', '.'))
                    }
                    self.pr_data.append(cleaned_row)
                    
            print(f"[OK] {len(self.pr_data)} Points de Reference charges avec succes")
            return True
            
        except FileNotFoundError:
            print(f"[ERREUR] Fichier {self.csv_file_path} non trouve")
            self.pr_data = []
            return False
        except Exception as e:
            print(f"[ERREUR] Erreur lors du chargement : {e}")
            self.pr_data = []
            return False
    
    def get_all_pr(self) -> List[Dict]:
        """
        Retourne tous les Points de Référence.
        
        Returns:
            List[Dict]: Liste de tous les PR avec leurs données
        """
        return self.pr_data
    
    def get_pr_count(self) -> int:
        """
        Retourne le nombre total de Points de Référence.
        
        Returns:
            int: Nombre de PR chargés
        """
        return len(self.pr_data)
    
    def search_pr_by_codes(self, codeCI: str = None, codeCH: str = None) -> List[Dict]:
        """
        Recherche des PR par codes CI et/ou CH.
        
        Args:
            codeCI (str, optional): Code CI à rechercher
            codeCH (str, optional): Code CH à rechercher
            
        Returns:
            List[Dict]: Liste des PR correspondants
        """
        results = []
        
        for pr in self.pr_data:
            match_ci = codeCI is None or pr['codeCI'] == codeCI
            match_ch = codeCH is None or pr['codeCH'] == codeCH
            
            if match_ci and match_ch:
                results.append(pr)
        
        return results
    
    def get_coordinates_for_map(self) -> List[Tuple[float, float, str, str, str]]:
        """
        Retourne les coordonnées formatées pour la cartographie.
        
        Returns:
            List[Tuple]: Liste de tuples (lat, lon, codeCI, codeCH, libelle)
        """
        coordinates = []
        
        for pr in self.pr_data:
            # Les coordonnées sont déjà en Lambert 93
            # Pour Leaflet, on peut les utiliser directement
            x = pr['XLambert93']
            y = pr['YLambert93']
            
            coordinates.append((
                x,  # X en Lambert 93 (abscisse)
                y,  # Y en Lambert 93 (ordonnée)
                pr['codeCI'],
                pr['codeCH'],
                pr['libelleCI']
            ))
        
        return coordinates


# Test du module si execute directement
if __name__ == "__main__":
    print("[TEST] Test du module DataManager")
    
    # Creer une instance du gestionnaire
    dm = DataManager()
    
    # Afficher quelques statistiques
    print(f"Nombre total de PR : {dm.get_pr_count()}")
    
    # Afficher les 5 premiers PR
    print("\nPremiers PR :")
    for i, pr in enumerate(dm.get_all_pr()[:5]):
        print(f"  {i+1}. {pr['codeCI']}-{pr['codeCH']} : {pr['libelleCI']}")
    
    print("\n[OK] Test termine")
