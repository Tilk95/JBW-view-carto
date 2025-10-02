"""
Module de génération de cartes pour JBW Viewer
==============================================

Ce module génère des cartes interactives Leaflet avec les Points de Référence (PR)
en utilisant la librairie Folium.

Auteur: Assistant IA
Date: 2025
Version: 1.0
"""

import folium
import folium.plugins
import os
from pyproj import Transformer
from typing import List, Tuple
from .data_manager import DataManager


class MapGenerator:
    """
    Générateur de cartes interactives pour les Points de Référence.
    
    Cette classe s'occupe de :
    - Créer des cartes Leaflet avec Folium
    - Positionner les marqueurs des PR
    - Générer des fichiers HTML pour l'affichage
    """
    
    def __init__(self, data_manager: DataManager):
        """
        Initialise le générateur de cartes.
        
        Args:
            data_manager (DataManager): Instance du gestionnaire de données
        """
        self.data_manager = data_manager
        self.map = None
        self.output_dir = "output"
        self._create_output_dir()
        
        # Initialiser le convertisseur de coordonnées Lambert 93 -> WGS84
        self.transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    
    def _create_output_dir(self) -> None:
        """
        Crée le dossier de sortie pour les cartes générées.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"[OK] Dossier de sortie cree : {self.output_dir}")
    
    def _lambert93_to_wgs84(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convertit les coordonnées Lambert 93 en WGS84 (latitude/longitude).
        
        Args:
            x (float): Coordonnée X en Lambert 93
            y (float): Coordonnée Y en Lambert 93
            
        Returns:
            Tuple[float, float]: (longitude, latitude) en WGS84
        """
        # Utiliser pyproj pour la conversion Lambert 93 -> WGS84
        lon, lat = self.transformer.transform(x, y)
        return lat, lon
    
    def create_map(self, center_lat: float = 46.0, center_lon: float = 2.0, zoom_start: int = 6) -> folium.Map:
        """
        Crée une carte Leaflet centrée sur la France.
        
        Args:
            center_lat (float): Latitude du centre de la carte
            center_lon (float): Longitude du centre de la carte
            zoom_start (int): Niveau de zoom initial
            
        Returns:
            folium.Map: Carte Leaflet configurée
        """
        # Créer la carte avec le fond OpenStreetMap uniquement
        self.map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        print("[OK] Carte Leaflet creee avec succes")
        return self.map
    
    def add_pr_markers(self, max_markers: int = 1000) -> None:
        """
        Ajoute les marqueurs des Points de Référence sur la carte.
        
        Args:
            max_markers (int): Nombre maximum de marqueurs à afficher
        """
        if not self.map:
            print("[ERREUR] Carte non initialisee")
            return
        
        # Récupérer les coordonnées des PR
        coordinates = self.data_manager.get_coordinates_for_map()
        
        # Limiter le nombre de marqueurs pour les performances
        if len(coordinates) > max_markers:
            print(f"[INFO] Limitation a {max_markers} marqueurs sur {len(coordinates)} PR disponibles")
            coordinates = coordinates[:max_markers]
        
        # Créer un groupe de marqueurs pour l'organisation (masqué par défaut)
        marker_cluster = folium.plugins.MarkerCluster(
            name='Points de Référence',
            overlay=True,
            control=True,
            show=False  # Masqué par défaut
        ).add_to(self.map)
        
        # Ajouter chaque marqueur
        for lambert_x, lambert_y, codeCI, codeCH, libelle in coordinates:
            # Convertir les coordonnées Lambert 93 en WGS84
            lat, lon = self._lambert93_to_wgs84(lambert_x, lambert_y)
            
            # Vérifier s'il y a une description personnalisée
            pr_key = f"{codeCI}-{codeCH}"
            custom_description = pr_descriptions.get(pr_key, None)
            
            # Créer le popup avec les informations du PR
            popup_text = f"""
            <div style='font-family: Arial, sans-serif;'>
                <h4>Point Remarquable</h4>
                <p><strong>Libellé:</strong> {libelle}</p>
                <p><strong>PR:</strong> {codeCI}.{codeCH}</p>"""
            
            # Ajouter la description personnalisée si elle existe
            if custom_description:
                popup_text += f"""
                <p><strong>Description:</strong><br>
                <span style='color: blue;'>{custom_description}</span></p>"""
            
            popup_text += f"""
            </div>
            """
            
            # Créer le marqueur
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"{codeCI}-{codeCH}: {libelle}",
                icon=folium.Icon(
                    color='blue',
                    icon='info-sign',
                    prefix='fa'
                )
            ).add_to(marker_cluster)
        
        print(f"[OK] {len(coordinates)} marqueurs ajoutes a la carte")
    
    def add_specific_pr_markers(self, pr_codes: List[Tuple[str, str]], pr_descriptions: dict = None, max_markers: int = 100) -> None:
        """
        Ajoute des marqueurs pour des PR spécifiques directement sur la carte.
        
        Args:
            pr_codes (List[Tuple[str, str]]): Liste de tuples (codeCI, codeCH) à afficher
            pr_descriptions (dict): Dictionnaire des descriptions optionnelles {codeCI-codeCH: description}
            max_markers (int): Nombre maximum de marqueurs à afficher
        """
        if not self.map:
            print("[ERREUR] Carte non initialisee")
            return
        
        # Initialiser le dictionnaire des descriptions si non fourni
        if pr_descriptions is None:
            pr_descriptions = {}
        
        # Récupérer les coordonnées des PR spécifiés
        coordinates = []
        for codeCI, codeCH in pr_codes:
            prs = self.data_manager.search_pr_by_codes(codeCI=codeCI, codeCH=codeCH)
            for pr in prs:
                coordinates.append((
                    pr['XLambert93'],
                    pr['YLambert93'],
                    pr['codeCI'],
                    pr['codeCH'],
                    pr['libelleCI']
                ))
        
        if not coordinates:
            print("[INFO] Aucun PR trouve pour les codes specifies")
            return
        
        # Limiter le nombre de marqueurs
        if len(coordinates) > max_markers:
            print(f"[INFO] Limitation a {max_markers} marqueurs sur {len(coordinates)} PR trouves")
            coordinates = coordinates[:max_markers]
        
        # Ajouter chaque marqueur directement sur la carte (sans couche de contrôle)
        for lambert_x, lambert_y, codeCI, codeCH, libelle in coordinates:
            # Convertir les coordonnées Lambert 93 en WGS84
            lat, lon = self._lambert93_to_wgs84(lambert_x, lambert_y)
            
            # Vérifier s'il y a une description personnalisée
            pr_key = f"{codeCI}-{codeCH}"
            custom_description = pr_descriptions.get(pr_key, None)
            
            # Créer le popup avec les informations du PR
            popup_text = f"""
            <div style='font-family: Arial, sans-serif;'>
                <h4>Point Remarquable</h4>
                <p><strong>Libellé:</strong> {libelle}</p>
                <p><strong>PR:</strong> {codeCI}.{codeCH}</p>"""
            
            # Ajouter la description personnalisée si elle existe
            if custom_description:
                popup_text += f"""
                <p><strong>Description:</strong><br>
                <span style='color: blue;'>{custom_description}</span></p>"""
            
            popup_text += f"""
            </div>
            """
            
            # Créer le marqueur directement sur la carte
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"{codeCI}-{codeCH}: {libelle}",
                icon=folium.Icon(
                    color='red',  # Couleur rouge pour les PR sélectionnés
                    icon='star',
                    prefix='fa'
                )
            ).add_to(self.map)
        
        print(f"[OK] {len(coordinates)} marqueurs PR selectionnes ajoutes a la carte")
    
    def add_legend(self) -> None:
        """
        Ajoute une légende à la carte.
        """
        if not self.map:
            return
        
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 60px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>JBW Viewer</b></p>
        <p>Cliquez sur un marqueur pour plus d'informations</p>
        </div>
        '''
        
        self.map.get_root().html.add_child(folium.Element(legend_html))
    
    def save_map(self, filename: str = "pr_map.html") -> str:
        """
        Sauvegarde la carte dans un fichier HTML.
        
        Args:
            filename (str): Nom du fichier de sortie
            
        Returns:
            str: Chemin complet du fichier généré
        """
        if not self.map:
            print("[ERREUR] Carte non initialisee")
            return None
        
        filepath = os.path.join(self.output_dir, filename)
        self.map.save(filepath)
        
        print(f"[OK] Carte sauvegardee : {filepath}")
        return filepath
    
    def generate_complete_map(self, filename: str = "pr_map.html", max_markers: int = 1000) -> str:
        """
        Génère une carte complète avec tous les éléments.
        
        Args:
            filename (str): Nom du fichier de sortie
            max_markers (int): Nombre maximum de marqueurs
            
        Returns:
            str: Chemin du fichier généré
        """
        print("[INFO] Generation de la carte complete...")
        
        # Créer la carte
        self.create_map()
        
        # Ajouter les marqueurs
        self.add_pr_markers(max_markers)
        
        # Ajouter la légende
        self.add_legend()
        
        # Ajouter le contrôle des couches
        folium.LayerControl().add_to(self.map)
        
        # Sauvegarder
        filepath = self.save_map(filename)
        
        print("[OK] Carte complete generee avec succes")
        return filepath
    
    def generate_map_with_specific_pr(self, pr_codes: List[Tuple[str, str]], pr_descriptions: dict = None, filename: str = "pr_specific_map.html") -> str:
        """
        Génère une carte avec des PR spécifiques.
        
        Args:
            pr_codes (List[Tuple[str, str]]): Liste de tuples (codeCI, codeCH) à afficher
            pr_descriptions (dict): Dictionnaire des descriptions optionnelles {codeCI-codeCH: description}
            filename (str): Nom du fichier de sortie
            
        Returns:
            str: Chemin du fichier généré
        """
        print("[INFO] Generation de la carte avec PR specifiques...")
        
        # Créer la carte
        self.create_map()
        
        # Ajouter les marqueurs spécifiques
        self.add_specific_pr_markers(pr_codes, pr_descriptions)
        
        # Ajouter la légende
        self.add_legend()
        
        # Pas de contrôle des couches (interface simplifiée)
        
        # Sauvegarder
        filepath = self.save_map(filename)
        
        print("[OK] Carte avec PR specifiques generee avec succes")
        return filepath


# Test du module si execute directement
if __name__ == "__main__":
    print("[TEST] Test du module MapGenerator")
    
    # Creer les instances necessaires
    dm = DataManager()
    mg = MapGenerator(dm)
    
    # Generer une carte de test
    filepath = mg.generate_complete_map("test_map.html", max_markers=50)
    
    if filepath:
        print(f"[OK] Carte de test generee : {filepath}")
    else:
        print("[ERREUR] Erreur lors de la generation de la carte")
