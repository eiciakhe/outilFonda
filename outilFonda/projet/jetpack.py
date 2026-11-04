"""Partie 1 : quel carburant pour faire 30 km jusqu'à l'IUT ?"""

import os
import matplotlib.pyplot as plt

RHO = 0.8                 # masse volumique du kérosène (kg/L), hypothèse
MASSE_SECHE = 120         # pilote + jetpack, sans carburant (kg)
CONSO_REF = 4.5 / 60      # consommation à 120 kg (L/s), d'après le grand oral
VITESSE = 100 / 3.6       # vitesse de croisière (m/s)
DISTANCE = 30_000         # maison -> IUT (m)
DOSSIER = os.path.dirname(os.path.abspath(__file__))  # dossier de ce fichier


def distance_parcourue(volume, dt=1.0):
    """Distance (m) faite avant la panne sèche, en partant de `volume` litres.

    Simulation par pas de dt secondes : plus il reste de carburant,
    plus le jetpack est lourd, donc plus il consomme.
    """
    if volume < 0:
        raise ValueError("le volume doit etre positif")
    temps = 0.0
    reste = volume
    while reste > 0:
        masse = MASSE_SECHE + RHO * reste
        reste = reste - CONSO_REF * (masse / MASSE_SECHE) * dt
        temps = temps + dt
    return VITESSE * temps


def dichotomie(f, a, b, tol=1e-3):
    """Racine de f entre a et b, avec f(a) < 0 < f(b)."""
    while b - a > tol:
        c = (a + b) / 2
        if f(c) < 0:
            a = c
        else:
            b = c
    return (a + b) / 2


def carburant_necessaire(dt=1.0):
    """Volume (L) qui permet d'atteindre exactement DISTANCE."""
    return dichotomie(lambda v: distance_parcourue(v, dt) - DISTANCE, 0, 500)


if __name__ == "__main__":
    print(f"Carburant nécessaire : {carburant_necessaire():.1f} L")

    pas = [10, 5, 2, 1, 0.5, 0.1]
    resultats = []
    for dt in pas:
        v = carburant_necessaire(dt)
        resultats.append(v)
        print(f"dt = {dt} s -> {v:.2f} L")

    plt.figure()
    plt.plot(pas, resultats, "o-")
    plt.xscale("log")
    plt.ylim(100, 110)          # échelle réaliste : la courbe est presque plate
    plt.xlabel("pas de temps dt (s)")
    plt.ylabel("carburant nécessaire pour 30 km (L)")
    plt.title("Le résultat dépend-il du pas de temps ?\n"
              "(écart de moins de 1 L sur 107 L)")
    plt.savefig(os.path.join(DOSSIER, "erreur_dt.png"))
