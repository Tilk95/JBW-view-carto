# 📖 MODE OPÉRATOIRE ULTRA SIMPLE - JBW Viewer

> **Pour les débutants** : Ce guide vous accompagne étape par étape pour installer et utiliser JBW Viewer.

---

## 🎯 QU'EST-CE QUE JBW VIEWER ?

**JBW Viewer** est un programme qui affiche des **Points de Référence** sur une **carte interactive**.

**En gros** : Vous donnez des codes (comme `597120-BA`), et le programme vous montre où ils se trouvent sur une carte de France.

---

## 📋 CE DONT VOUS AVEZ BESOIN

### ✅ Vérifications avant de commencer

1. **Votre ordinateur** : Windows, Mac ou Linux
2. **Python installé** : Vérifiez en ouvrant un terminal et tapez `python --version`
   - Si ça marche → ✅ Parfait !
   - Si ça ne marche pas → Voir section "Installation de Python" ci-dessous

---

## 🚀 ÉTAPE 1 : INSTALLATION DE PYTHON

### Si Python n'est pas installé :

1. **Allez sur** : https://www.python.org/downloads/
2. **Cliquez sur** : "Download Python 3.x" (le gros bouton vert)
3. **Lancez le fichier** téléchargé
4. **IMPORTANT** : Cochez "Add Python to PATH" ✅
5. **Cliquez** : "Install Now"
6. **Attendez** que l'installation se termine
7. **Redémarrez** votre ordinateur

### Vérification :
- Ouvrez un terminal (cmd sur Windows)
- Tapez : `python --version`
- Vous devriez voir : `Python 3.x.x`

---

## 📁 ÉTAPE 2 : TÉLÉCHARGEMENT DU PROJET

### Option A : Si vous avez Git
```bash
git clone [URL_DU_REPOSITORY]
cd JBW-view-carto
```

### Option B : Si vous n'avez pas Git
1. **Téléchargez** le projet en ZIP
2. **Extrayez** le fichier ZIP
3. **Ouvrez** un terminal dans le dossier `JBW-view-carto`

---

## ⚙️ ÉTAPE 3 : INSTALLATION DES DÉPENDANCES

**Dans le terminal, tapez exactement :**

```bash
pip install -r requirements.txt
```

**Vous devriez voir :**
```
Successfully installed folium-0.14.0 pyproj-3.6.0
```

**Si ça ne marche pas :**
```bash
python -m pip install -r requirements.txt
```

---

## 🎮 ÉTAPE 4 : UTILISATION SIMPLE

### 🖱️ MODE 1 : Interface graphique (le plus simple)

1. **Ouvrez un terminal** dans le dossier du projet
2. **Tapez :**
   ```bash
   python main.py
   ```
3. **Une fenêtre s'ouvre** avec des boutons
4. **Dans la zone de texte**, tapez vos codes PR :
   ```
   597120-BA
   142091-AO
   393314-BV
   ```
5. **Cliquez sur "Générer la carte"**
6. **Cliquez sur "Ouvrir la carte"**
7. **Votre navigateur s'ouvre** avec la carte !

### 📄 MODE 2 : Avec un fichier (plus rapide)

1. **Créez un fichier** `mes_pr.txt` avec vos codes :
   ```
   597120-BA
   142091-AO
   393314-BV
   ```
2. **Dans le terminal, tapez :**
   ```bash
   python main.py mes_pr.txt
   ```
3. **La carte s'ouvre automatiquement** dans votre navigateur !

---

## 📝 FORMAT DES CODES PR

### Format simple :
```
597120-BA
142091-AO
393314-BV
```

### Format avec descriptions (optionnel) :
```
597120-BA;Site historique d'Argenton-sur-Creuse
142091-AO;Monument de Langres
393314-BV;Château de Rambouillet
```

---

## 🗺️ COMMENT LIRE LA CARTE

1. **Marqueurs rouges** : Vos Points de Référence
2. **Cliquez sur un marqueur** : Informations détaillées
3. **Zoom** : Molette de la souris
4. **Déplacer** : Clic-glisser

---

## ❌ PROBLÈMES COURANTS

### "Python n'est pas reconnu"
- **Solution** : Python n'est pas installé ou pas dans le PATH
- **Refaire** : Étape 1 (Installation de Python)

### "Module not found"
- **Solution** : Les dépendances ne sont pas installées
- **Refaire** : Étape 3 (Installation des dépendances)

### "Fichier CSV non trouvé"
- **Solution** : Le fichier `TTH_EXPLORER_REFERENTIEL_PR.csv` doit être dans le dossier
- **Vérifier** : Que tous les fichiers du projet sont présents

### "Aucun PR trouvé"
- **Solution** : Vérifiez que vos codes existent dans la base
- **Exemple valide** : `597120-BA`, `142091-AO`

---

## 🆘 AIDE RAPIDE

### Commandes utiles :
```bash
python main.py --help          # Aide détaillée
python main.py exemple_pr.txt  # Test avec fichier d'exemple
```

### Fichiers d'exemple fournis :
- `exemple_pr.txt` : Codes PR simples
- `exemple_pr_avec_descriptions.txt` : Codes avec descriptions

---

## ✅ RÉCAPITULATIF ULTRA RAPIDE

1. **Installer Python** (si pas déjà fait)
2. **Télécharger le projet**
3. **Installer les dépendances** : `pip install -r requirements.txt`
4. **Lancer** : `python main.py`
5. **Saisir vos codes PR** dans l'interface
6. **Générer et ouvrir** la carte

**C'est tout !** 🎉

---

## 📞 BESOIN D'AIDE ?

1. **Lisez** ce guide étape par étape
2. **Vérifiez** que Python est installé
3. **Vérifiez** que tous les fichiers sont présents
4. **Testez** avec les fichiers d'exemple fournis

**JBW Viewer** - Simple, rapide, efficace ! 🗺️✨
