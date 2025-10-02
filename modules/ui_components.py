"""
Module d'interface utilisateur pour JBW Viewer
==============================================

Ce module gère l'interface utilisateur Tkinter de l'application desktop.

Auteur: Assistant IA
Date: 2025
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os
from typing import Callable
from .data_manager import DataManager
from .map_generator import MapGenerator


class JBWViewerUI:
    """
    Interface utilisateur principale de l'application JBW Viewer.
    
    Cette classe gère :
    - L'interface Tkinter principale
    - Les contrôles utilisateur (boutons, champs de saisie)
    - L'interaction avec les modules de données et cartes
    """
    
    def __init__(self):
        """
        Initialise l'interface utilisateur.
        """
        self.root = tk.Tk()
        self.data_manager = None
        self.map_generator = None
        self.setup_ui()
        
        # Charger automatiquement les données au démarrage
        self.auto_load_data()
    
    def auto_load_data(self) -> None:
        """
        Charge automatiquement les données au démarrage de l'application.
        """
        try:
            self.update_status("Chargement automatique des données...")
            self.data_manager = DataManager()
            
            if self.data_manager.get_pr_count() > 0:
                # Mettre à jour l'interface pour refléter le chargement automatique
                self.data_status.config(text="✅ Données chargées automatiquement")
                self.data_info.config(text=f"{self.data_manager.get_pr_count()} Points de Référence disponibles")
                self.generate_btn.config(state='normal')
                self.search_btn.config(state='normal')
                self.add_info(f"✅ {self.data_manager.get_pr_count()} Points de Référence chargés automatiquement au démarrage")
            else:
                self.data_status.config(text="❌ Erreur de chargement automatique")
                self.add_info("❌ Aucune donnée chargée automatiquement")
                
        except Exception as e:
            self.data_status.config(text="❌ Erreur de chargement automatique")
            self.add_info(f"❌ Erreur lors du chargement automatique : {e}")
        finally:
            self.update_status("Prêt - Données chargées")
    
    def setup_ui(self) -> None:
        """
        Configure l'interface utilisateur principale.
        """
        # Configuration de la fenêtre principale
        self.root.title("JBW Viewer - Visualiseur de Points de Référence")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Style de l'interface
        style = ttk.Style()
        style.theme_use('clam')
        
        # Créer le conteneur principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre de l'application
        title_label = ttk.Label(
            main_frame, 
            text="🗺️ JBW Viewer", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Section de chargement des données
        self.create_data_section(main_frame)
        
        # Section de PR spécifiques
        self.create_specific_pr_section(main_frame)
        
        # Section d'informations
        self.create_info_section(main_frame)
        
        # Boutons d'action
        self.create_action_buttons(main_frame)
        
        # Barre de statut
        self.create_status_bar(main_frame)
    
    def create_data_section(self, parent: ttk.Frame) -> None:
        """
        Crée la section de gestion des données.
        
        Args:
            parent: Widget parent
        """
        # Frame pour la section données
        data_frame = ttk.LabelFrame(parent, text="📊 Données", padding="10")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Bouton de rechargement des données
        self.load_btn = ttk.Button(
            data_frame,
            text="Recharger les données CSV",
            command=self.load_data
        )
        self.load_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Label de statut des données
        self.data_status = ttk.Label(data_frame, text="Chargement en cours...")
        self.data_status.grid(row=0, column=1)
        
        # Informations sur les données
        self.data_info = ttk.Label(data_frame, text="")
        self.data_info.grid(row=1, column=0, columnspan=2, pady=(5, 0))
    
    def create_map_section(self, parent: ttk.Frame) -> None:
        """
        Crée la section de génération de cartes.
        
        Args:
            parent: Widget parent
        """
        # Frame pour la section cartes
        map_frame = ttk.LabelFrame(parent, text="🗺️ Cartes", padding="10")
        map_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Contrôles de génération de carte
        controls_frame = ttk.Frame(map_frame)
        controls_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Limite de marqueurs
        ttk.Label(controls_frame, text="Limite de marqueurs:").grid(row=0, column=0, padx=(0, 5))
        self.max_markers_var = tk.StringVar(value="1000")
        max_markers_entry = ttk.Entry(controls_frame, textvariable=self.max_markers_var, width=10)
        max_markers_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Bouton de génération de carte
        self.generate_btn = ttk.Button(
            controls_frame,
            text="Générer la carte",
            command=self.generate_map,
            state='disabled'
        )
        self.generate_btn.grid(row=0, column=2)
        
        # Bouton d'ouverture de la carte
        self.open_btn = ttk.Button(
            controls_frame,
            text="Ouvrir la carte",
            command=self.open_map,
            state='disabled'
        )
        self.open_btn.grid(row=0, column=3, padx=(10, 0))
        
        # Statut de la carte
        self.map_status = ttk.Label(map_frame, text="Aucune carte générée")
        self.map_status.grid(row=1, column=0, columnspan=2, pady=(5, 0))
    
    def create_specific_pr_section(self, parent: ttk.Frame) -> None:
        """
        Crée la section pour les PR spécifiques.
        
        Args:
            parent: Widget parent
        """
        # Frame pour la section PR spécifiques
        pr_frame = ttk.LabelFrame(parent, text="🎯 Génération de cartes avec PR spécifiques", padding="10")
        pr_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zone de saisie des codes PR
        input_frame = ttk.Frame(pr_frame)
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Titre et options de saisie
        title_frame = ttk.Frame(input_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(title_frame, text="Codes PR (format: CI-CH, un par ligne):").grid(row=0, column=0, sticky=tk.W)
        
        # Bouton pour charger un fichier
        self.load_file_btn = ttk.Button(
            title_frame,
            text="Charger depuis fichier",
            command=self.load_pr_from_file
        )
        self.load_file_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Zone de texte pour saisir les codes
        self.pr_codes_text = tk.Text(input_frame, height=4, width=50, wrap=tk.WORD)
        self.pr_codes_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Scrollbar pour la zone de texte
        pr_scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.pr_codes_text.yview)
        pr_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=(5, 0))
        self.pr_codes_text.configure(yscrollcommand=pr_scrollbar.set)
        
        # Boutons d'action
        button_frame = ttk.Frame(pr_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Bouton de génération de carte
        self.generate_btn = ttk.Button(
            button_frame,
            text="Générer la carte",
            command=self.generate_specific_map,
            state='disabled'
        )
        self.generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Bouton d'ouverture de la carte
        self.open_btn = ttk.Button(
            button_frame,
            text="Ouvrir la carte",
            command=self.open_specific_map,
            state='disabled'
        )
        self.open_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Bouton d'exemple
        self.example_btn = ttk.Button(
            button_frame,
            text="Exemple",
            command=self.load_example_pr
        )
        self.example_btn.grid(row=0, column=2)
        
        # Statut de la carte
        self.map_status = ttk.Label(pr_frame, text="Aucune carte générée")
        self.map_status.grid(row=2, column=0, columnspan=2, pady=(5, 0))
    
    def create_info_section(self, parent: ttk.Frame) -> None:
        """
        Crée la section d'informations.
        
        Args:
            parent: Widget parent
        """
        # Frame pour les informations
        info_frame = ttk.LabelFrame(parent, text="ℹ️ Informations", padding="10")
        info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zone de texte pour les informations
        self.info_text = tk.Text(info_frame, height=8, width=70, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar pour la zone de texte
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        # Informations initiales
        self.add_info("Bienvenue dans JBW Viewer !")
        self.add_info("1. Les données CSV sont chargées automatiquement au démarrage")
        self.add_info("2. Saisissez des codes PR au format CI-CH (un par ligne)")
        self.add_info("3. Ou chargez un fichier contenant les codes PR")
        self.add_info("4. Générez la carte avec les PR sélectionnés")
        self.add_info("5. Ouvrez la carte dans votre navigateur")
    
    def create_action_buttons(self, parent: ttk.Frame) -> None:
        """
        Crée les boutons d'action principaux.
        
        Args:
            parent: Widget parent
        """
        # Frame pour les boutons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # Bouton de recherche
        self.search_btn = ttk.Button(
            button_frame,
            text="Rechercher un PR",
            command=self.search_pr,
            state='disabled'
        )
        self.search_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Bouton de quitter
        quit_btn = ttk.Button(
            button_frame,
            text="Quitter",
            command=self.root.quit
        )
        quit_btn.grid(row=0, column=1)
    
    def create_status_bar(self, parent: ttk.Frame) -> None:
        """
        Crée la barre de statut.
        
        Args:
            parent: Widget parent
        """
        self.status_var = tk.StringVar(value="Prêt")
        status_label = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def add_info(self, message: str) -> None:
        """
        Ajoute un message à la zone d'informations.
        
        Args:
            message (str): Message à ajouter
        """
        self.info_text.insert(tk.END, f"{message}\n")
        self.info_text.see(tk.END)
    
    def update_status(self, message: str) -> None:
        """
        Met à jour le message de statut.
        
        Args:
            message (str): Nouveau message de statut
        """
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def load_data(self) -> None:
        """
        Recharge les données CSV (utilisé pour le rechargement manuel).
        """
        try:
            self.update_status("Rechargement des données...")
            self.data_manager = DataManager()
            
            if self.data_manager.get_pr_count() > 0:
                self.data_status.config(text="✅ Données rechargées")
                self.data_info.config(text=f"{self.data_manager.get_pr_count()} Points de Référence disponibles")
                self.generate_btn.config(state='normal')
                self.search_btn.config(state='normal')
                self.add_info(f"✅ {self.data_manager.get_pr_count()} Points de Référence rechargés avec succès")
            else:
                self.data_status.config(text="❌ Erreur de rechargement")
                self.add_info("❌ Aucune donnée rechargée")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du rechargement : {e}")
            self.add_info(f"❌ Erreur : {e}")
        finally:
            self.update_status("Prêt - Données rechargées")
    
    def generate_map(self) -> None:
        """
        Génère la carte des Points de Référence.
        """
        try:
            if not self.data_manager:
                messagebox.showwarning("Attention", "Veuillez d'abord charger les données")
                return
            
            self.update_status("Génération de la carte...")
            
            # Récupérer la limite de marqueurs
            try:
                max_markers = int(self.max_markers_var.get())
            except ValueError:
                max_markers = 1000
            
            # Créer le générateur de cartes
            self.map_generator = MapGenerator(self.data_manager)
            
            # Générer la carte
            filepath = self.map_generator.generate_complete_map(
                filename="pr_map.html",
                max_markers=max_markers
            )
            
            if filepath:
                self.map_status.config(text=f"✅ Carte générée : {os.path.basename(filepath)}")
                self.open_btn.config(state='normal')
                self.add_info(f"✅ Carte générée avec succès : {filepath}")
                self.add_info(f"📍 {min(max_markers, self.data_manager.get_pr_count())} marqueurs affichés")
            else:
                self.map_status.config(text="❌ Erreur de génération")
                self.add_info("❌ Erreur lors de la génération de la carte")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {e}")
            self.add_info(f"❌ Erreur : {e}")
        finally:
            self.update_status("Prêt")
    
    def open_map(self) -> None:
        """
        Ouvre la carte dans le navigateur par défaut.
        """
        try:
            if self.map_generator:
                filepath = os.path.join("output", "pr_map.html")
                if os.path.exists(filepath):
                    webbrowser.open(f"file://{os.path.abspath(filepath)}")
                    self.add_info("🌐 Carte ouverte dans le navigateur")
                else:
                    messagebox.showwarning("Attention", "Aucune carte générée trouvée")
            else:
                messagebox.showwarning("Attention", "Veuillez d'abord générer une carte")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture : {e}")
    
    def search_pr(self) -> None:
        """
        Ouvre une fenêtre de recherche de PR.
        """
        if not self.data_manager:
            messagebox.showwarning("Attention", "Veuillez d'abord charger les données")
            return
        
        # Créer une fenêtre de recherche
        search_window = tk.Toplevel(self.root)
        search_window.title("Recherche de Points de Référence")
        search_window.geometry("400x300")
        
        # Interface de recherche
        ttk.Label(search_window, text="Rechercher un PR").pack(pady=10)
        
        # Champ de recherche
        search_frame = ttk.Frame(search_window)
        search_frame.pack(pady=10)
        
        ttk.Label(search_frame, text="Code CI:").grid(row=0, column=0, padx=(0, 5))
        ci_entry = ttk.Entry(search_frame)
        ci_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(search_frame, text="Code CH:").grid(row=0, column=2, padx=(0, 5))
        ch_entry = ttk.Entry(search_frame)
        ch_entry.grid(row=0, column=3)
        
        # Zone de résultats
        results_text = tk.Text(search_window, height=10, width=50)
        results_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        def do_search():
            results_text.delete(1.0, tk.END)
            ci = ci_entry.get().strip()
            ch = ch_entry.get().strip()
            
            if not ci and not ch:
                results_text.insert(tk.END, "Veuillez saisir au moins un code")
                return
            
            results = self.data_manager.search_pr_by_codes(
                codeCI=ci if ci else None,
                codeCH=ch if ch else None
            )
            
            if results:
                results_text.insert(tk.END, f"Trouvé {len(results)} résultat(s) :\n\n")
                for pr in results[:20]:  # Limiter à 20 résultats
                    results_text.insert(tk.END, 
                        f"• {pr['codeCI']}-{pr['codeCH']} : {pr['libelleCI']}\n"
                        f"  Coordonnées: X={pr['XLambert93']:.2f}, Y={pr['YLambert93']:.2f}\n\n"
                    )
                if len(results) > 20:
                    results_text.insert(tk.END, f"... et {len(results) - 20} autres résultats")
            else:
                results_text.insert(tk.END, "Aucun résultat trouvé")
        
        # Bouton de recherche
        ttk.Button(search_window, text="Rechercher", command=do_search).pack(pady=10)
    
    def generate_specific_map(self) -> None:
        """
        Génère une carte avec des PR spécifiques.
        """
        try:
            if not self.data_manager:
                messagebox.showwarning("Attention", "Veuillez d'abord charger les données")
                return
            
            # Récupérer les codes PR saisis
            pr_text = self.pr_codes_text.get("1.0", tk.END).strip()
            if not pr_text:
                messagebox.showwarning("Attention", "Veuillez saisir au moins un code PR")
                return
            
            # Parser les codes PR
            pr_codes = []
            for line in pr_text.split('\n'):
                line = line.strip()
                if line and '-' in line:
                    try:
                        codeCI, codeCH = line.split('-', 1)
                        pr_codes.append((codeCI.strip(), codeCH.strip()))
                    except ValueError:
                        self.add_info(f"⚠️ Format invalide ignoré: {line}")
                        continue
            
            if not pr_codes:
                messagebox.showwarning("Attention", "Aucun code PR valide trouvé")
                return
            
            self.update_status("Génération de la carte avec PR spécifiques...")
            
            # Créer le générateur de cartes
            self.map_generator = MapGenerator(self.data_manager)
            
            # Générer la carte avec les PR spécifiques
            filepath = self.map_generator.generate_map_with_specific_pr(
                pr_codes=pr_codes,
                filename="pr_specific_map.html"
            )
            
            if filepath:
                self.map_status.config(text=f"✅ Carte générée : {os.path.basename(filepath)}")
                self.open_btn.config(state='normal')
                self.add_info(f"✅ Carte générée avec {len(pr_codes)} PR : {filepath}")
            else:
                self.map_status.config(text="❌ Erreur de génération")
                self.add_info("❌ Erreur lors de la génération de la carte")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {e}")
            self.add_info(f"❌ Erreur : {e}")
        finally:
            self.update_status("Prêt")
    
    def open_specific_map(self) -> None:
        """
        Ouvre la carte dans le navigateur.
        """
        try:
            if self.map_generator:
                filepath = os.path.join("output", "pr_specific_map.html")
                if os.path.exists(filepath):
                    webbrowser.open(f"file://{os.path.abspath(filepath)}")
                    self.add_info("🌐 Carte ouverte dans le navigateur")
                else:
                    messagebox.showwarning("Attention", "Aucune carte générée trouvée")
            else:
                messagebox.showwarning("Attention", "Veuillez d'abord générer une carte")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture : {e}")
    
    def load_example_pr(self) -> None:
        """
        Charge des exemples de codes PR.
        """
        example_codes = """597120-BA
142091-AO
393314-BV
583005-FP
726158-ST"""
        
        self.pr_codes_text.delete("1.0", tk.END)
        self.pr_codes_text.insert("1.0", example_codes)
        self.add_info("📝 Exemples de codes PR chargés")
    
    def load_pr_from_file(self) -> None:
        """
        Charge des codes PR depuis un fichier.
        """
        try:
            # Ouvrir une boîte de dialogue pour sélectionner un fichier
            file_path = filedialog.askopenfilename(
                title="Sélectionner un fichier de codes PR",
                filetypes=[
                    ("Fichiers texte", "*.txt"),
                    ("Fichiers CSV", "*.csv"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if file_path:
                # Lire le fichier
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                
                # Charger le contenu dans la zone de texte
                self.pr_codes_text.delete("1.0", tk.END)
                self.pr_codes_text.insert("1.0", content)
                
                # Compter le nombre de codes
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                valid_codes = [line for line in lines if '-' in line]
                
                self.add_info(f"📁 Fichier chargé : {os.path.basename(file_path)}")
                self.add_info(f"📊 {len(valid_codes)} codes PR valides trouvés")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement du fichier : {e}")
            self.add_info(f"❌ Erreur lors du chargement : {e}")
    
    def load_pr_from_file_path(self, file_path: str) -> None:
        """
        Charge des codes PR depuis un fichier fourni en argument.
        
        Args:
            file_path (str): Chemin vers le fichier de codes PR
        """
        try:
            # Lire le fichier
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            
            # Charger le contenu dans la zone de texte
            self.pr_codes_text.delete("1.0", tk.END)
            self.pr_codes_text.insert("1.0", content)
            
            # Compter le nombre de codes
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            valid_codes = [line for line in lines if '-' in line]
            
            self.add_info(f"📁 Fichier chargé au démarrage : {os.path.basename(file_path)}")
            self.add_info(f"📊 {len(valid_codes)} codes PR valides trouvés")
            
        except Exception as e:
            self.add_info(f"❌ Erreur lors du chargement du fichier : {e}")
    
    def auto_generate_map(self) -> None:
        """
        Génère automatiquement la carte avec les PR chargés.
        """
        try:
            if not self.data_manager:
                self.add_info("❌ Aucune donnée disponible pour la génération automatique")
                self.close_application()
                return
            
            # Récupérer les codes PR saisis
            pr_text = self.pr_codes_text.get("1.0", tk.END).strip()
            if not pr_text:
                self.add_info("❌ Aucun code PR saisi pour la génération automatique")
                self.close_application()
                return
            
            # Parser les codes PR avec description optionnelle
            pr_codes = []
            pr_descriptions = {}
            invalid_lines = []
            for line_num, line in enumerate(pr_text.split('\n'), 1):
                line = line.strip()
                if line and '-' in line:
                    try:
                        # Séparer le code PR de la description (optionnelle)
                        if ';' in line:
                            pr_part, description = line.split(';', 1)
                            description = description.strip()
                        else:
                            pr_part = line
                            description = None
                        
                        # Parser le code PR
                        codeCI, codeCH = pr_part.split('-', 1)
                        codeCI = codeCI.strip()
                        codeCH = codeCH.strip()
                        
                        pr_codes.append((codeCI, codeCH))
                        if description:
                            pr_descriptions[f"{codeCI}-{codeCH}"] = description
                            
                    except ValueError:
                        invalid_lines.append(f"Ligne {line_num}: {line}")
                elif line:  # Ligne non vide mais sans tiret
                    invalid_lines.append(f"Ligne {line_num}: {line}")
            
            if not pr_codes:
                self.add_info("❌ Aucun code PR valide trouvé dans le fichier")
                if invalid_lines:
                    self.add_info("❌ Format invalide détecté :")
                    for invalid in invalid_lines[:5]:  # Limiter à 5 erreurs
                        self.add_info(f"   - {invalid}")
                self.close_application()
                return
            
            # Vérifier que les PR existent dans le référentiel
            found_prs = []
            for codeCI, codeCH in pr_codes:
                prs = self.data_manager.search_pr_by_codes(codeCI=codeCI, codeCH=codeCH)
                if prs:
                    found_prs.extend(prs)
            
            if not found_prs:
                self.add_info("❌ Aucun PR trouvé dans le référentiel pour les codes fournis")
                self.add_info(f"❌ Codes recherchés : {len(pr_codes)} codes")
                self.close_application()
                return
            
            self.update_status("Génération automatique de la carte...")
            
            # Créer le générateur de cartes
            self.map_generator = MapGenerator(self.data_manager)
            
            # Générer la carte avec les PR spécifiques
            filepath = self.map_generator.generate_map_with_specific_pr(
                pr_codes=pr_codes,
                pr_descriptions=pr_descriptions,
                filename="auto_generated_map.html"
            )
            
            if filepath:
                self.map_status.config(text=f"✅ Carte générée automatiquement : {os.path.basename(filepath)}")
                self.open_btn.config(state='normal')
                self.add_info(f"✅ Carte générée automatiquement avec {len(found_prs)} PR trouvés : {filepath}")
                
                # Ouvrir automatiquement la carte
                self.auto_open_map(filepath)
            else:
                self.map_status.config(text="❌ Erreur de génération automatique")
                self.add_info("❌ Erreur lors de la génération automatique de la carte")
                self.close_application()
                
        except Exception as e:
            self.add_info(f"❌ Erreur lors de la génération automatique : {e}")
            self.close_application()
        finally:
            self.update_status("Prêt - Carte générée automatiquement")
    
    def auto_open_map(self, filepath: str) -> None:
        """
        Ouvre automatiquement la carte dans le navigateur et ferme l'application.
        
        Args:
            filepath (str): Chemin vers le fichier de carte
        """
        try:
            webbrowser.open(f"file://{os.path.abspath(filepath)}")
            self.add_info("🌐 Carte ouverte automatiquement dans le navigateur")
            self.add_info("🔄 Fermeture de l'application...")
            
            # Fermer l'application après un court délai
            self.root.after(2000, self.close_application)
            
        except Exception as e:
            self.add_info(f"⚠️ Impossible d'ouvrir automatiquement la carte : {e}")
    
    def close_application(self) -> None:
        """
        Ferme l'application proprement.
        """
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
    
    def run(self) -> None:
        """
        Lance l'application.
        """
        self.root.mainloop()


# Test du module si exécuté directement
if __name__ == "__main__":
    print("🧪 Test du module UI Components")
    
    # Créer et lancer l'interface
    app = JBWViewerUI()
    app.run()
