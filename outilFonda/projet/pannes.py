"""Partie 3 : risque. Que se passe-t-il si le moteur perd de la poussée ?

Scénario : le pilote est immobile à une hauteur h quand le moteur perd
un pourcentage `perte` de sa poussée. Pendant DELAI secondes il ne réagit
pas (poussée = poids, amputée de la panne), puis il met les gaz à fond
(poussée maximale, amputée de la panne).
On regarde à quelle vitesse il touche le sol.
"""

import os
import random
import matplotlib.pyplot as plt

DOSSIER = os.path.dirname(os.path.abspath(__file__))

MASSE = 120             # kg (grand oral)
G = 10                  # m/s^2 (grand oral)
POUSSEE_MAX = 1800      # N (grand oral, 1,5 g ressenti)
DELAI = 1.0             # s de réaction du pilote (HYPOTHÈSE)
SEUIL = 5.0             # m/s, HYPOTHÈSE du modèle : environ une chute de 1,25 m


def vitesse_impact(perte, hauteur, dt=0.01):
    """Vitesse (m/s) au sol, ou 0 si le pilote a pu se rattraper."""
    h = hauteur
    v = 0.0                     # vitesse vers le haut (négative = on tombe)
    pas_delai = round(DELAI / dt)   # nombre de pas sans réaction (entier)
    pas = 0
    while h > 0:
        if pas < pas_delai:
            poussee = (1 - perte) * MASSE * G
        else:
            poussee = (1 - perte) * POUSSEE_MAX
        a = (poussee - MASSE * G) / MASSE
        v = v + a * dt
        h = h + v * dt
        pas = pas + 1
        if pas >= pas_delai and v >= 0:
            return 0.0          # le pilote ne tombe plus : sauvé
    return -v


def proportion_crash(perte, n=1000):
    """Part de vols (sur n) qui finissent à plus de SEUIL m/s."""
    crashs = 0
    for _ in range(n):
        hauteur = random.uniform(10, 100)
        if vitesse_impact(perte, hauteur) > SEUIL:
            crashs = crashs + 1
    return crashs / n


if __name__ == "__main__":
    random.seed(42)             # tirages reproductibles

    # Vérification : le pas dt change-t-il la vitesse d'impact ?
    for dt in [0.1, 0.01, 0.001]:
        print(f"dt = {dt} -> {vitesse_impact(0.4, 50, dt):.3f} m/s")

    # Pas de 5 % partout, sauf entre 30 et 40 % où la bascule a lieu (pas de 1 %)
    pertes = ([p / 100 for p in range(0, 30, 5)]
              + [p / 100 for p in range(30, 41)]
              + [p / 100 for p in range(45, 65, 5)])
    proportions = []
    for perte in pertes:
        prop = proportion_crash(perte)
        proportions.append(prop)
        print(f"perte {perte:.0%} -> {prop:.1%} de crashs")

    plt.figure()
    plt.plot([p * 100 for p in pertes], [q * 100 for q in proportions], "o-",
             markersize=4)
    plt.axvline(100 / 3, color="red", linestyle="--",
                label="perte critique : 1/3 (poussée = poids)")
    plt.xlabel("perte de poussée (%)")
    plt.ylabel("vols touchant le sol à plus de 5 m/s (%)")
    plt.title("Part des vols qui finissent à plus de 5 m/s\n"
              "(1000 vols par niveau de panne, départ entre 10 et 100 m)")
    plt.legend()
    plt.savefig(os.path.join(DOSSIER, "pannes.png"))
