# 🗺️ JBW Viewer - Visualisateur de Points de Référence

Application desktop de visualisation interactive de Points de Référence (PR) sur carte OpenStreetMap.

## 📋 Description

**JBW Viewer** est une application Python légère qui permet de visualiser des Points de Référence (PR) sur une carte interactive. L'application utilise OpenStreetMap et Leaflet pour une expérience cartographique fluide.

### ✨ Fonctionnalités

- **Visualisation interactive** : Carte Leaflet avec OpenStreetMap
- **Chargement automatique** : Données de référence chargées au démarrage
- **Recherche de PR** : Localisation par codes CI-CH
- **Descriptions personnalisées** : Support des descriptions optionnelles
- **Mode automatique** : Génération de carte via fichier en paramètre
- **Interface graphique** : Interface Tkinter intuitive
- **Conversion de coordonnées** : Lambert 93 vers WGS84 automatique

## 🚀 Installation

> **📖 Pour les débutants** : Consultez le [MODE_OPERATOIRE_SIMPLE.md](MODE_OPERATOIRE_SIMPLE.md) pour un guide étape par étape ultra simple !

### Prérequis

- **Python 3.7+** installé sur votre système
- **Git** (optionnel, pour cloner le repository)

### Installation des dépendances

1. **Cloner ou télécharger** le projet :
```bash
git clone <repository-url>
cd JBW-view-carto
```

2. **Installer les dépendances Python** :
```bash
pip install -r requirements.txt
```

### Dépendances requises

- `folium>=0.14.0` : Cartographie interactive
- `pyproj>=3.0.0` : Conversion de coordonnées Lambert 93 → WGS84
- `tkinter` : Interface graphique (inclus avec Python)

## 📁 Structure du projet

```
JBW-view-carto/
├── main.py                          # Point d'entrée principal
├── requirements.txt                 # Dépendances Python
├── TTH_EXPLORER_REFERENTIEL_PR.csv # Base de données des PR (9,962 PR)
├── modules/
│   ├── data_manager.py             # Gestion des données CSV
│   ├── map_generator.py            # Génération des cartes Leaflet
│   └── ui_components.py            # Interface utilisateur Tkinter
├── output/                         # Cartes générées (créé automatiquement)
└── exemple_pr.txt                  # Fichier d'exemple de PR
```

## 🚀 Démarrage rapide

### Pour les débutants (Windows)
1. **Double-cliquez** sur `DEMARRER_JBW_VIEWER.bat`
2. **Suivez** les instructions à l'écran
3. **C'est tout !** 🎉

### Pour les débutants (Mac/Linux)
1. **Lancez** le test : `python TEST_SIMPLE.py`
2. **Suivez** le [MODE_OPERATOIRE_SIMPLE.md](MODE_OPERATOIRE_SIMPLE.md)
3. **C'est tout !** 🎉

## 🎯 Utilisation

### Mode interactif (Interface graphique)

Lancer l'application avec l'interface graphique :

```bash
python main.py
```

**Interface disponible :**
- **Saisie de PR** : Zone de texte pour entrer les codes PR
- **Chargement fichier** : Bouton pour charger un fichier de PR
- **Génération** : Bouton pour créer la carte
- **Ouverture** : Bouton pour ouvrir la carte dans le navigateur

### Mode automatique (Fichier en paramètre)

Générer automatiquement une carte avec un fichier de PR :

```bash
python main.py mon_fichier_pr.txt
```

**Comportement :**
- Charge les PR du fichier
- Génère la carte automatiquement
- Ouvre la carte dans le navigateur
- Ferme l'application après génération

### Format des fichiers PR

**Format de base :**
```
597120-BA
142091-AO
393314-BV
583005-FP
726158-ST
```

**Format avec descriptions (optionnel) :**
```
597120-BA;Site historique d'Argenton-sur-Creuse
142091-AO;Monument de Langres
393314-BV;Château de Rambouillet
583005-FP
```

## 📊 Exemples d'utilisation

### 1. Lancement normal
```bash
python main.py
```
→ Ouvre l'interface graphique

### 2. Génération automatique
```bash
python main.py exemple_pr.txt
```
→ Génère et ouvre la carte automatiquement

### 3. Aide
```bash
python main.py --help
```
→ Affiche l'aide détaillée

## 🗺️ Fonctionnalités de la carte

### Marqueurs
- **Icône** : Étoile rouge
- **Popup** : Informations du PR
  - Titre : "Point Remarquable"
  - Libellé : Nom du point
  - PR : Code identifiant (CI.CH)
  - Description : Texte personnalisé (si présent)

### Navigation
- **Zoom** : Molette de la souris
- **Déplacement** : Clic-glisser
- **Informations** : Clic sur un marqueur

## 🔧 Configuration

### Base de données
- **Fichier** : `TTH_EXPLORER_REFERENTIEL_PR.csv`
- **Format** : CSV avec colonnes codeCI, codeCH, libelleCI, XLambert93, YLambert93
- **Coordonnées** : Lambert 93 (conversion automatique vers WGS84)

### Cartes générées
- **Dossier** : `output/`
- **Format** : HTML avec Leaflet
- **Nommage** : `auto_generated_map.html` (mode auto) ou `pr_specific_map.html` (mode manuel)

## 🐛 Dépannage

### Erreurs courantes

**1. Fichier CSV non trouvé :**
```
[ERREUR] Fichier TTH_EXPLORER_REFERENTIEL_PR.csv non trouvé
```
→ Vérifier que le fichier est présent dans le dossier racine

**2. Aucun PR trouvé :**
```
[ERREUR] Aucun PR trouvé dans le référentiel
```
→ Vérifier les codes PR dans le fichier d'entrée

**3. Format de fichier invalide :**
```
[ERREUR] Format invalide détecté
```
→ Vérifier le format : `codeCI-codeCH` ou `codeCI-codeCH;description`

### Logs de débogage

L'application affiche des messages de statut :
- `[OK]` : Opération réussie
- `[INFO]` : Information
- `[ERREUR]` : Erreur critique

## 📝 Développement

### Architecture modulaire

- **`data_manager.py`** : Gestion des données CSV
- **`map_generator.py`** : Génération des cartes Folium/Leaflet
- **`ui_components.py`** : Interface utilisateur Tkinter
- **`main.py`** : Point d'entrée et logique principale

### Ajout de fonctionnalités

1. **Nouvelle fonctionnalité** : Ajouter dans le module approprié
2. **Interface** : Modifier `ui_components.py`
3. **Tests** : Créer des scripts de test
4. **Documentation** : Mettre à jour ce README

## 📄 Licence

Application développée pour la visualisation de Points de Référence.

## 🤝 Support

Pour toute question ou problème :
1. Vérifier les logs d'erreur
2. Consulter la section Dépannage
3. Vérifier le format des fichiers d'entrée

---

**JBW Viewer** - Visualisation simple et efficace de Points de Référence 🗺️✨
