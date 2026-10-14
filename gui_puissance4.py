"""Interface graphique (tkinter) pour puissance4.py.

Lancement :
    python gui_puissance4.py                      -> humain (rouge) vs minmax2@4 (jaune)
    python gui_puissance4.py human human          -> deux humains
    python gui_puissance4.py minmax1@3 minmax2@3  -> IA contre IA
"""
import sys
import tkinter as tk

from puissance4 import puissance4

COULEURS = {0: "white", 1: "#e8101a", 2: "#f5a30a"}
NOMS = {1: "Rouge", 2: "Jaune"}


class interfaceGraphique:
    def __init__(self, jeu, taille=80, delai_ia=300):
        self._jeu = jeu
        self._taille = taille
        self._delai_ia = delai_ia
        self._fini = False
        self._after_id = None

        self._root = tk.Tk()
        self._root.title("Puissance 4")
        self._canvas = tk.Canvas(self._root,
                                 width=jeu.m * taille, height=jeu.n * taille,
                                 bg="#1d4e9e", highlightthickness=0)
        self._canvas.pack()
        self._canvas.bind("<Button-1>", self._clic)

        bas = tk.Frame(self._root)
        bas.pack(fill="x", pady=4)
        self._statut = tk.Label(bas, text="", font=("Arial", 13))
        self._statut.pack(side="left", padx=8)
        tk.Button(bas, text="Nouvelle partie",
                  command=self.nouvelle_partie).pack(side="right", padx=8)

    # ----- Affichage ------------------------------------------------------
    def _dessiner(self):
        t = self._taille
        self._canvas.delete("all")
        for r in range(self._jeu.n):
            for c in range(self._jeu.m):
                couleur = COULEURS[self._jeu.plateau[r][c]]
                self._canvas.create_oval(c * t + 8, r * t + 8,
                                         (c + 1) * t - 8, (r + 1) * t - 8,
                                         fill=couleur, outline="#0b2a5c", width=2)

    def _message(self, texte):
        self._statut.config(text=texte)
        self._root.update_idletasks()

    # ----- Déroulement de la partie --------------------------------------
    def nouvelle_partie(self):
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None
        self._jeu.reinitialiser()
        self._fini = False
        self._dessiner()
        self._prochain_tour()

    def _prochain_tour(self):
        joueur = self._jeu.joueur_courant
        if self._jeu.joueur_est_humain(joueur):
            self._message(f"{NOMS[joueur]} : cliquez sur une colonne")
        else:
            self._message(f"{NOMS[joueur]} (ordinateur) réfléchit...")
            self._after_id = self._root.after(self._delai_ia, self._coup_ordi)

    def _coup_ordi(self):
        self._after_id = None
        if self._fini:
            return
        c = self._jeu.choisir_coup_joueur(self._jeu.joueur_courant)
        self._jouer(c)

    def _clic(self, event):
        if self._fini or self._jeu.joueur_est_humain(self._jeu.joueur_courant) is False:
            return
        c = event.x // self._taille
        if self._jeu.peut_jouer(c):
            self._jouer(c)

    def _jouer(self, c):
        joueur = self._jeu.joueur_courant
        self._jeu.poser_pion(c)
        self._dessiner()
        if self._jeu.est_gagnant(c):
            self._fini = True
            self._message(f"{NOMS[joueur]} gagne !")
        elif self._jeu.plateau_plein():
            self._fini = True
            self._message("Match nul.")
        else:
            self._prochain_tour()

    def lancer(self):
        self.nouvelle_partie()
        self._root.mainloop()


if __name__ == "__main__":
    j1 = sys.argv[1] if len(sys.argv) > 1 else "human"
    j2 = sys.argv[2] if len(sys.argv) > 2 else "minmax2@4"
    interfaceGraphique(puissance4(type_j1=j1, type_j2=j2)).lancer()
