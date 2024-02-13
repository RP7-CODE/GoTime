import tkinter as tk
from tkinter import ttk
import asyncio
from datetime import datetime
import platform
import webbrowser
from tkinter import messagebox

systeme_exploitation = platform.system()
lien_du_github = "https://github.com/RP7-CODE/GoTime"
nom_application = "GoTime"
type_application = "DESKTOP"
theme_sombre_couleur_hexa = "#242424"
taille_de_la_fenetre = "1080x720"
couleur_frame_minuteur_verte = "#73FF14"
couleur_frame_minuteur_jaune = "#F4EF12"
couleur_frame_minuteur_rouge = "#F84615"
temps_max_supporte_par_le_minuteur = 3600*3 # 10800

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # ------------------------ Variables pour les paramètre du minuteur
        self.paused = False
        self.time_remaining = None
        self.valeur_state_bouton_start = None
        # ------------------------ Paramètrage de la fenêtre.
        self.title(f"{nom_application} - Application {type_application} - {systeme_exploitation}")
        self.geometry(taille_de_la_fenetre)
        self.minsize(1000, 680)
        self.config(background=theme_sombre_couleur_hexa)
        # ------------------------ Barre de menu
        barre_de_menu = tk.Menu(self)
        # ------------------------ création d'un premier menu 'fenêtre'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="paramètres", command=self.fonction_pour_la_page_des_parametres)
        fenetre_menu.add_command(label="close page", command=self.quit)
        barre_de_menu.add_cascade(label="Fenêtre", menu=fenetre_menu)
        # ------------------------ création d'un second menu 'Aide'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="Open source", command=self.open_github)
        fenetre_menu.add_command(label="Show source", command=self.show_github)
        barre_de_menu.add_cascade(label="Aide", menu=fenetre_menu)
        # ------------------------ création d'un troisième menu 'commandes'
        commandes_menu = tk.Menu(barre_de_menu, tearoff=0)
        commandes_menu.add_command(label="start", command=self.start_timer)
        commandes_menu.add_command(label="pause", command=self.pause_timer)
        commandes_menu.add_command(label="stop", command=self.stop_timer)
        commandes_menu.add_command(label="clear entry", command=self.clear_entrees)
        barre_de_menu.add_cascade(label="Commandes", menu=commandes_menu)
        # ------------------------ Ajout de la barre de menu à la fenêtre
        self.config(menu=barre_de_menu)
        # ------------------------ Affichage de l'heure en haut de la fenêtre
        self.time_label = tk.Label(self, text="", font=("Arial", 24), bg="#242424", fg="white")
        self.time_label.pack(pady=20)
        # ------------------------ Création de la frame de couleur et affichage d'un texte dedans (ici le temps restant)
        self.time_frame = tk.Frame(self, bg=couleur_frame_minuteur_verte, height=80)
        self.time_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.temps_restant_label = tk.Label(self.time_frame, text=f"{nom_application}", font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
        self.temps_restant_label.pack(pady=20)
        # ------------------------ Boutons pour la gestion du minuteur
        self.boutons_frame = tk.Frame(self, bg=theme_sombre_couleur_hexa, height=80)
        self.boutons_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.bouton_start = tk.Button(self.boutons_frame, text="START",
                                      activebackground=couleur_frame_minuteur_verte,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.start_timer)
        self.valeur_state_bouton_start = False
        self.bouton_pause = tk.Button(self.boutons_frame, text="PAUSE",
                                      activebackground=couleur_frame_minuteur_verte,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.pause_timer)
        self.bouton_stop = tk.Button(self.boutons_frame, text="STOP",
                                     activebackground=couleur_frame_minuteur_verte,
                                     state="disabled", width=30, height=2,
                                     justify="center", relief="groove",
                                     command=self.stop_timer)
        self.bouton_start.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_pause.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_stop.pack(side="left", padx=10, pady=10, expand=True)
        # ------------------------ Entrées pour la gestion du temps du minuteur (minutes et secondes)
        # ------------ Entrée des minutes :
        self.entrees_frame = tk.Frame(self, bg=theme_sombre_couleur_hexa)
        self.entrees_frame.pack(padx=20, pady=(0, 20))
        self.minutes_entry = tk.Entry(self.entrees_frame, width=40)
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.bind('<Return>', self.start_timer)
        self.minutes_entry.pack(side="left", padx=(20, 10), expand=True)
        # ------------ Entrée des secondes :
        self.seconds_entry = tk.Entry(self.entrees_frame, width=40)
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.bind('<Return>', self.start_timer)
        self.seconds_entry.pack(side="left", padx=(10, 20), expand=True)
        # ------------ Boutons pour effacer les entrées
        self.bouton_clear_entrees = tk.Button(self.entrees_frame, text="Effacer les entrées", activebackground=couleur_frame_minuteur_jaune,width=15,command=self.clear_entrees)
        self.bouton_clear_entrees.pack(side="left", padx=10, pady=20, expand=True)
        # ------------------------ Mise à jour de l'heure et activation de la gestion des entrées
        self.update_time()
        self.get_entrees()

    def get_entrees(self):
        if self.seconds_entry.get() or self.minutes_entry.get() != 0:
            if self.valeur_state_bouton_start == True:
                pass
            elif self.valeur_state_bouton_start == False:
                self.bouton_start.config(state="normal")
                self.valeur_state_bouton_start = True
        else:
            if self.valeur_state_bouton_start == True:
                self.bouton_start.config(state="disabled")
                self.valeur_state_bouton_start = False
            elif self.valeur_state_bouton_start == False:
                pass
        self.after(50, self.get_entrees)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Met à jour toutes les secondes

    def start_timer(self):
        minutes = int(self.minutes_entry.get())
        seconds = int(self.seconds_entry.get())
        self.total_seconds = minutes * 60 + seconds
        self.time_remaining = self.total_seconds
        if self.time_remaining >= temps_max_supporte_par_le_minuteur:
            messagebox.showwarning(f"WARNING !\nLe temps total de seconde du minuteur ne peut pas dépasser {temps_max_supporte_par_le_minuteur}s !\nMerci d'entrer un temps de durée inferieur !")
        else:
            self.minutes_entry.config(state="disabled")
            self.seconds_entry.config(state="disabled")
            self.bouton_start.config(state="disabled")
            self.valeur_state_bouton_start = False
            self.bouton_clear_entrees.config(state="disabled")
            self.bouton_pause.config(state="normal")
            self.bouton_stop.config(state="normal")
            self.update_timer()

    def update_timer(self):
        if self.time_remaining > 0 and not self.paused:
            self.time_remaining -= 1
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.temps_restant_label.config(text=time_str, font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
            # Calcul des pourcentages
            total_time = self.total_seconds
            time_left = self.time_remaining
            percent_remaining = time_left / total_time
            # Changement de couleur en fonction du pourcentage restant
            if percent_remaining <= 0.2:
                self.time_frame.config(bg=couleur_frame_minuteur_rouge)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_rouge)
            elif percent_remaining <= 0.3:
                self.time_frame.config(bg=couleur_frame_minuteur_jaune)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_jaune)
            else:
                self.time_frame.config(bg=couleur_frame_minuteur_verte)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_verte)
            self.after(1000, self.update_timer)
        elif self.paused:
            pass  # Pause le minuteur sans décrémenter le temps
        else:
            self.time_frame.config(bg=couleur_frame_minuteur_verte)
            self.temps_restant_label.config(text="Terminé!", font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
            self.stop_timer(True)

    def pause_timer(self):
        if not hasattr(self, 'paused'):
            self.paused = False
        else:
            self.paused = not self.paused
            if self.paused:
                self.bouton_pause.config(text="REPRENDRE")
            else:
                self.bouton_pause.config(text="PAUSE")
                self.update_timer()

    def stop_timer(self, parametre_appel_bouton_ou_non = None):
        self.time_remaining = 0  # Réinitialiser le temps restant
        self.bouton_start.config(state="normal")
        self.valeur_state_bouton_start = True
        self.bouton_pause.config(state="disabled")
        self.bouton_stop.config(state="disabled")
        self.minutes_entry.config(state="normal")
        self.seconds_entry.config(state="normal")
        self.bouton_clear_entrees.config(state="normal")
        self.temps_restant_label.config(text=f"{nom_application}", font=("Arial", 24))
        if parametre_appel_bouton_ou_non == None:
            self.update_timer()  # Arrêter la récursion de la fonction update_timer()
        else:
            pass

    def fonction_pour_la_page_des_parametres(self):
        print("Ouverture de la page des paramètres !")
        fenetre_parametres = tk.Toplevel(self, width=200, height=300)
        progressBar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=100)
        progressBar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        progressBar.start(); asyncio.sleep(1); progressBar.stop(); progressBar.destroy()
        label_titre_parametres = tk.Label(fenetre_parametres, text=f"{nom_application}", font=("Arial", 24))
        label_titre_parametres.pack(pady=10, expand=True)

    def show_github(self):
        messagebox.showinfo(f"Source {nom_application}", f"Lien du GitHub du projet :\n{lien_du_github}")
        print("Ouverture de la fenêtre d'information pour afficher le lien du github !")

    def open_github(self):
        print(f"Ouverture du github de {nom_application} dans une nouvelle fenêtre de navigateur !")
        webbrowser.open_new(lien_du_github)

    def clear_entrees(self):
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.insert(0, "0")

if __name__ == "__main__":
    root = Application()
    root.mainloop()