"""TP Puissance 4 généralisé (n lignes, m colonnes, p pions à aligner) + MinMax."""
import random

INF = float("inf")
VICTOIRE = 10_000  # valeur d'une position gagnante dans MinMax


# --------------------------------------------------------------------------
# 2 - Classe puissance4
# --------------------------------------------------------------------------
class puissance4:
    SYMBOLES = {0: " ", 1: "x", 2: "o"}

    def __init__(self, n=6, m=7, p=4,
                 type_j1="human", type_j2="human",
                 profondeur=4, elagage=True):
        """type_j1 / type_j2 : "human", "stupid", "minmax1" ou "minmax2"
        (minmax1 = heuristique 1, minmax2 = heuristique 2)."""
        self._n, self._m, self._p = n, m, p
        self._profondeur = profondeur
        self._elagage = elagage
        self._joueur_courant = 1
        self._plateau = [[0] * m for _ in range(n)]
        self._calculer_blocs()
        self._joueurs = {1: self._creer_joueur(type_j1),
                         2: self._creer_joueur(type_j2)}

    # ----- Getters / Setters -------------------------------------------
    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def p(self):
        return self._p

    @n.setter
    def n(self, v):
        self._n = v
        self.reinitialiser()

    @m.setter
    def m(self, v):
        self._m = v
        self.reinitialiser()

    @p.setter
    def p(self, v):
        self._p = v
        self.reinitialiser()

    @property
    def plateau(self):
        return self._plateau

    @plateau.setter
    def plateau(self, v):
        self._plateau = v

    @property
    def joueur_courant(self):
        return self._joueur_courant

    @joueur_courant.setter
    def joueur_courant(self, v):
        self._joueur_courant = v

    @property
    def blocs(self):
        return self._blocs

    @property
    def scores_cases(self):
        return self._scores_cases

    # ----- Préparation des heuristiques ---------------------------------
    def _calculer_blocs(self):
        """Liste de tous les blocs de p cases alignées + score de chaque case
        (= nombre de blocs passant par la case)."""
        n, m, p = self._n, self._m, self._p
        self._blocs = []
        self._scores_cases = [[0] * m for _ in range(n)]
        for r in range(n):
            for c in range(m):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    r2, c2 = r + (p - 1) * dr, c + (p - 1) * dc
                    if 0 <= r2 < n and 0 <= c2 < m:
                        bloc = [(r + k * dr, c + k * dc) for k in range(p)]
                        self._blocs.append(bloc)
                        for (a, b) in bloc:
                            self._scores_cases[a][b] += 1

    def reinitialiser(self):
        self._plateau = [[0] * self._m for _ in range(self._n)]
        self._joueur_courant = 1
        self._calculer_blocs()

    # ----- Méthodes du plateau ------------------------------------------
    def afficher(self):
        for ligne in self._plateau:
            print("|" + "|".join(self.SYMBOLES[x] for x in ligne) + "|")
        print(" " + " ".join("-" * self._m))
        print(" " + " ".join(str(c + 1) for c in range(self._m)))
        print()

    def nb_pions_colonne(self, c):
        return sum(1 for r in range(self._n) if self._plateau[r][c] != 0)

    def peut_jouer(self, c):
        return 0 <= c < self._m and self.nb_pions_colonne(c) < self._n

    def colonnes_jouables(self):
        return [c for c in range(self._m) if self.peut_jouer(c)]

    def poser_pion(self, c):
        """Pose un pion du joueur courant dans la colonne c, puis passe la
        main à l'adversaire. Retourne la ligne où le pion est tombé."""
        r = self._n - 1 - self.nb_pions_colonne(c)
        self._plateau[r][c] = self._joueur_courant
        self._joueur_courant = 3 - self._joueur_courant
        return r

    def retirer_pion(self, c):
        """Annule le dernier pion posé dans la colonne c (utile pour MinMax)."""
        r = self._n - self.nb_pions_colonne(c)
        self._plateau[r][c] = 0
        self._joueur_courant = 3 - self._joueur_courant

    def est_gagnant(self, c):
        """Le dernier pion posé dans la colonne c fait-il gagner son joueur ?"""
        nb = self.nb_pions_colonne(c)
        if nb == 0:
            return False
        r = self._n - nb
        couleur = self._plateau[r][c]
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            compte = 1
            for sens in (1, -1):
                a, b = r + sens * dr, c + sens * dc
                while (0 <= a < self._n and 0 <= b < self._m
                       and self._plateau[a][b] == couleur):
                    compte += 1
                    a, b = a + sens * dr, b + sens * dc
            if compte >= self._p:
                return True
        return False

    # ----- 5 - Parties entre joueurs -------------------------------------
    def _creer_joueur(self, type_joueur):
        # Syntaxe "minmax2@5" : profondeur 5 pour ce joueur uniquement.
        nom, _, prof = type_joueur.partition("@")
        profondeur = int(prof) if prof else self._profondeur
        if nom == "human":
            return human(self)
        if nom == "stupid":
            return stupidBot(self)
        if nom in ("minmax1", "minmax2"):
            return minMax(self, profondeur, self._elagage, int(nom[-1]))
        raise ValueError(f"Type de joueur inconnu : {type_joueur}")

    def definir_joueurs(self, type_j1, type_j2):
        self._joueurs = {1: self._creer_joueur(type_j1),
                         2: self._creer_joueur(type_j2)}

    def joueur_est_humain(self, joueur):
        return isinstance(self._joueurs[joueur], human)

    def choisir_coup_joueur(self, joueur):
        """Demande son coup au joueur (1 ou 2) sans le jouer."""
        return self._joueurs[joueur].choisir_coup()

    def plateau_plein(self):
        return not self.colonnes_jouables()

    def jouer_partie(self, affichage=True):
        """Fait s'affronter les deux joueurs. Retourne 1, 2 (vainqueur) ou 0
        (match nul)."""
        self.reinitialiser()
        while True:
            if affichage:
                self.afficher()
            joueur = self._joueur_courant
            c = self._joueurs[joueur].choisir_coup()
            self.poser_pion(c)
            if self.est_gagnant(c):
                if affichage:
                    self.afficher()
                    print(f"Le joueur {joueur} ({self.SYMBOLES[joueur]}) gagne !")
                return joueur
            if not self.colonnes_jouables():
                if affichage:
                    self.afficher()
                    print("Match nul.")
                return 0


# --------------------------------------------------------------------------
# 3 - Classe minMax
# --------------------------------------------------------------------------
class minMax:
    def __init__(self, jeu, profondeur=4, elagage=True, heuristique=1):
        self._jeu = jeu
        self._profondeur = profondeur
        self._elagage = elagage
        self._heuristique = heuristique  # 1 ou 2

    @property
    def profondeur(self):
        return self._profondeur

    @profondeur.setter
    def profondeur(self, v):
        self._profondeur = v

    @property
    def elagage(self):
        return self._elagage

    @elagage.setter
    def elagage(self, v):
        self._elagage = v

    # ----- Heuristiques ---------------------------------------------------
    def evaluer(self, joueur):
        """Valeur de l'état courant du point de vue de `joueur`."""
        if self._heuristique == 1:
            return self._heuristique1(joueur)
        return self._heuristique2(joueur)

    def _heuristique1(self, joueur):
        jeu, total = self._jeu, 0
        for r in range(jeu.n):
            for c in range(jeu.m):
                case = jeu.plateau[r][c]
                if case == joueur:
                    total += jeu.scores_cases[r][c]
                elif case != 0:
                    total -= jeu.scores_cases[r][c]
        return total

    def _heuristique2(self, joueur):
        jeu, total = self._jeu, 0
        plateau = jeu.plateau
        for bloc in jeu.blocs:
            moi = adv = 0
            for (r, c) in bloc:
                v = plateau[r][c]
                if v == joueur:
                    moi += 1
                elif v != 0:
                    adv += 1
            if moi and adv:
                continue            # bloc mixte : score 0
            if moi:
                total += 2 ** moi   # score du bloc : 2^q
            elif adv:
                total -= 2 ** adv
        return total

    # ----- MinMax ---------------------------------------------------------
    def _ordre_colonnes(self):
        cols = self._jeu.colonnes_jouables()
        random.shuffle(cols)  # départage aléatoire des coups équivalents
        centre = (self._jeu.m - 1) / 2
        cols.sort(key=lambda c: abs(c - centre))  # centre d'abord : meilleur élagage
        return cols

    def _minmax(self, prof, alpha, beta, maximisant, racine):
        """Retourne (valeur, colonne). `racine` = joueur pour qui on optimise."""
        jeu = self._jeu
        cols = self._ordre_colonnes()
        if not cols:
            return 0, None  # plateau plein : nul
        meilleure_col = cols[0]
        meilleur = -INF if maximisant else INF
        for c in cols:
            jeu.poser_pion(c)
            if jeu.est_gagnant(c):
                val = (VICTOIRE + prof) if maximisant else -(VICTOIRE + prof)
            elif prof == 1:
                val = self.evaluer(racine)
            else:
                val, _ = self._minmax(prof - 1, alpha, beta, not maximisant, racine)
            jeu.retirer_pion(c)

            if maximisant and val > meilleur:
                meilleur, meilleure_col = val, c
                alpha = max(alpha, val)
            elif not maximisant and val < meilleur:
                meilleur, meilleure_col = val, c
                beta = min(beta, val)
            if self._elagage and alpha >= beta:
                break
        return meilleur, meilleure_col

    def choisir_coup(self):
        _, col = self._minmax(self._profondeur, -INF, INF, True,
                              self._jeu.joueur_courant)
        return col


# --------------------------------------------------------------------------
# 4 - Autres joueurs
# --------------------------------------------------------------------------
class stupidBot:
    def __init__(self, jeu):
        self._jeu = jeu

    def choisir_coup(self):
        return random.choice(self._jeu.colonnes_jouables())


class human:
    def __init__(self, jeu):
        self._jeu = jeu

    def choisir_coup(self):
        while True:
            saisie = input(f"Joueur {self._jeu.joueur_courant}, colonne "
                           f"(1-{self._jeu.m}) : ")
            if saisie.strip().isdigit() and self._jeu.peut_jouer(int(saisie) - 1):
                return int(saisie) - 1
            print("Coup invalide.")


# --------------------------------------------------------------------------
# 6 - Comparaison des performances
# --------------------------------------------------------------------------
def comparer(types, nb_parties=10, n=6, m=7, p=4, profondeur=3, elagage=True):
    """Chaque type affronte chacun des autres nb_parties fois, en alternant
    celui qui commence. Affiche les statistiques."""
    stats = {t: {"victoires": 0, "defaites": 0, "nuls": 0} for t in types}
    for i, a in enumerate(types):
        for b in types[i + 1:]:
            res = {"a": 0, "b": 0, "nul": 0}
            for k in range(nb_parties):
                if k % 2 == 0:
                    jeu = puissance4(n, m, p, a, b, profondeur, elagage)
                    gagnant = jeu.jouer_partie(affichage=False)
                    cle = {1: "a", 2: "b", 0: "nul"}[gagnant]
                else:
                    jeu = puissance4(n, m, p, b, a, profondeur, elagage)
                    gagnant = jeu.jouer_partie(affichage=False)
                    cle = {1: "b", 2: "a", 0: "nul"}[gagnant]
                res[cle] += 1
            print(f"{a:>8} vs {b:<8} : {res['a']} - {res['b']} "
                  f"({res['nul']} nuls)")
            stats[a]["victoires"] += res["a"]; stats[a]["defaites"] += res["b"]
            stats[b]["victoires"] += res["b"]; stats[b]["defaites"] += res["a"]
            stats[a]["nuls"] += res["nul"];    stats[b]["nuls"] += res["nul"]
    print("\nBilan :")
    for t, s in stats.items():
        print(f"{t:>8} : {s['victoires']} V / {s['defaites']} D / {s['nuls']} N")
    return stats


if __name__ == "__main__":
    # Exemple : humain contre MinMax (heuristique 2) :
    # puissance4(type_j1="human", type_j2="minmax2", profondeur=4).jouer_partie()
    comparer(["stupid", "minmax1", "minmax2"], nb_parties=10, profondeur=3)
