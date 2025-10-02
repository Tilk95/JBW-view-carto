"""
JBW Viewer - Application principale
===================================

Application desktop pour la visualisation de Points de Référence (PR)
sur une carte interactive utilisant OpenStreetMap et Leaflet.

Fonctionnalités :
- Chargement des données CSV des PR
- Génération de cartes interactives
- Recherche de PR par codes
- Interface utilisateur simple et intuitive

Auteur: Assistant IA
Date: 2025
Version: 1.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ajouter le dossier modules au path Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from modules.ui_components import JBWViewerUI
    from modules.data_manager import DataManager
    from modules.map_generator import MapGenerator
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    print("Vérifiez que tous les modules sont présents dans le dossier 'modules'")
    sys.exit(1)


def check_dependencies():
    """
    Vérifie que toutes les dépendances sont installées.
    
    Returns:
        bool: True si toutes les dépendances sont disponibles
    """
    missing_deps = []
    
    try:
        import folium
    except ImportError:
        missing_deps.append("folium")
    
    if missing_deps:
        error_msg = f"""
❌ Dépendances manquantes : {', '.join(missing_deps)}

Pour installer les dépendances manquantes, exécutez :
pip install -r requirements.txt

Ou installez manuellement :
pip install folium
        """
        print(error_msg)
        return False
    
    return True


def check_data_file():
    """
    Vérifie que le fichier de données CSV est présent.
    
    Returns:
        bool: True si le fichier existe
    """
    csv_path = "data/TTH_EXPLORER_REFERENTIEL_PR.csv"
    
    if not os.path.exists(csv_path):
        error_msg = f"""
❌ Fichier de données manquant : {csv_path}

Assurez-vous que le fichier CSV des Points de Référence est présent
dans le dossier 'data' de l'application.
        """
        print(error_msg)
        return False
    
    return True


def main():
    """
    Point d'entrée principal de l'application JBW Viewer.
    """
    print("Demarrage de JBW Viewer...")
    print("=" * 50)
    
    # Vérifications préliminaires
    print("Verification des dependances...")
    if not check_dependencies():
        return 1
    
    print("Verification du fichier de donnees...")
    if not check_data_file():
        return 1
    
    print("Toutes les verifications sont passees")
    print()
    
    try:
        # Créer et lancer l'interface utilisateur
        print("Lancement de l'interface utilisateur...")
        app = JBWViewerUI()
        
        # Vérifier si un fichier de PR a été fourni en argument
        if len(sys.argv) > 1 and sys.argv[1].endswith(('.txt', '.csv')):
            pr_file = sys.argv[1]
            if os.path.exists(pr_file):
                print(f"Chargement du fichier de PR : {pr_file}")
                app.load_pr_from_file_path(pr_file)
                
                # Générer automatiquement la carte
                print("Generation automatique de la carte...")
                app.auto_generate_map()
            else:
                print(f"Fichier non trouve : {pr_file}")
        
        # Afficher les informations de démarrage
        print("Application lancee avec succes")
        print("Consultez l'interface pour commencer")
        print()
        
        # Lancer la boucle principale
        app.run()
        
    except Exception as e:
        error_msg = f"❌ Erreur critique : {e}"
        print(error_msg)
        
        # Afficher une boîte de dialogue d'erreur si possible
        try:
            root = tk.Tk()
            root.withdraw()  # Masquer la fenêtre principale
            messagebox.showerror("Erreur Critique", error_msg)
        except:
            pass  # Si Tkinter ne fonctionne pas, on continue
        
        return 1
    
    print("Application fermee")
    return 0


def show_help():
    """
    Affiche l'aide de l'application.
    """
    help_text = """
JBW VIEWER - AIDE DETAILLEE
============================

DESCRIPTION:
    Application desktop de visualisation de Points de Référence (PR) sur carte 
    interactive OpenStreetMap. Interface graphique intuitive avec génération 
    automatique de cartes HTML.

SYNTAXE:
    python main.py [fichier_pr] [options]

ARGUMENTS:
    fichier_pr    Fichier contenant les codes PR (optionnel)
                  Format: un code par ligne au format CI-CH
                  Extensions supportées: .txt, .csv
                  Descriptions optionnelles: codeCI-codeCH;description

OPTIONS:
    -h, --help    Affiche cette aide détaillée
    help          Affiche cette aide détaillée

EXEMPLES D'UTILISATION:
    python main.py                    # Mode interactif (interface graphique)
    python main.py exemple_pr.txt     # Mode automatique avec fichier
    python main.py --help             # Affiche cette aide
    python main.py -h                 # Affiche cette aide

FORMATS DE FICHIER PR:

    Format de base:
    597120-BA
    142091-AO
    393314-BV
    583005-FP
    726158-ST

    Format avec descriptions (optionnel):
    597120-BA;Site historique d'Argenton-sur-Creuse
    142091-AO;Monument de Langres
    393314-BV;Château de Rambouillet
    583005-FP

MODES DE FONCTIONNEMENT:

    Mode interactif (sans fichier):
    - Lance l'interface graphique Tkinter
    - Saisie manuelle des codes PR
    - Chargement de fichier via interface
    - Génération et ouverture de cartes
    - Application reste ouverte

    Mode automatique (avec fichier):
    - Charge les PR du fichier spécifié
    - Génère la carte automatiquement
    - Ouvre la carte dans le navigateur
    - Ferme l'application après génération

FONCTIONNALITES PRINCIPALES:

    Cartographie:
    - Carte interactive OpenStreetMap
    - Marqueurs étoiles rouges pour les PR
    - Popups avec informations détaillées
    - Navigation zoom/déplacement
    - Conversion Lambert 93 -> WGS84

    Interface:
    - Zone de saisie de codes PR
    - Bouton de chargement de fichier
    - Boutons génération/ouverture
    - Barre de statut informative
    - Messages d'erreur détaillés

    Données:
    - 9,962 Points de Référence disponibles
    - Recherche par codes CI-CH
    - Descriptions personnalisées
    - Export HTML autonome

FICHIERS IMPORTANTS:

    Données:
    - TTH_EXPLORER_REFERENTIEL_PR.csv : Base de données (9,962 PR)
    - exemple_pr.txt : Fichier d'exemple simple
    - exemple_pr_avec_descriptions.txt : Fichier avec descriptions

    Génération:
    - output/ : Dossier des cartes générées
    - auto_generated_map.html : Carte mode automatique
    - pr_specific_map.html : Carte mode manuel

    Configuration:
    - requirements.txt : Dépendances Python
    - README.md : Documentation complète

GESTION D'ERREURS:

    Erreurs de fichier:
    - Fichier CSV manquant -> Arret de l'application
    - Fichier PR invalide -> Message d'erreur detaille
    - Format incorrect -> Liste des lignes problematiques

    Erreurs de donnees:
    - Aucun PR trouve -> Verification des codes
    - Codes invalides -> Affichage des erreurs
    - Conversion echouee -> Message d'erreur technique

    Logs de debogage:
    - [OK] : Operation reussie
    - [INFO] : Information generale
    - [ERREUR] : Erreur critique

DEPENDANCES REQUISES:

    Python 3.7+ avec modules:
    - folium>=0.14.0 : Cartographie interactive
    - pyproj>=3.0.0 : Conversion de coordonnees
    - tkinter : Interface graphique (inclus)

    Installation:
    pip install -r requirements.txt

AIDE SUPPLEMENTAIRE:

    Documentation complete:
    - README.md : Guide d'installation et d'utilisation
    - Structure du projet et architecture
    - Exemples detailles et depannage

    Support:
    - Verifier les logs d'erreur
    - Consulter la section Depannage du README
    - Verifier le format des fichiers d'entree

================================
JBW Viewer - Visualisation simple et efficace de Points de Reference
    """
    print(help_text)


if __name__ == "__main__":
    # Vérifier les arguments de ligne de commande
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        sys.exit(0)
    
    # Lancer l'application
    exit_code = main()
    sys.exit(exit_code)
