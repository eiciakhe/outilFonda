"""Partie 2 : existe-t-il une vitesse de croisière qui consomme le moins ?

Idée : à basse vitesse on vole longtemps, donc on brûle beaucoup pour rester
en l'air. À haute vitesse, le frottement de l'air (en v^2) fait consommer
davantage. Entre les deux, il y a peut-être un minimum.
"""

import math
import os
import matplotlib.pyplot as plt
import jetpack
from jetpack import RHO, MASSE_SECHE, DISTANCE, CONSO_REF, VITESSE, dichotomie

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# HYPOTHÈSE du modèle (pas une donnée du grand oral) :
# 2/3 de la conso sert à tenir en l'air, 1/3 à vaincre l'air à 100 km/h.
PART_VOL = 2 / 3
CONSO_VOL = CONSO_REF * PART_VOL
K_AIR = (CONSO_REF - CONSO_VOL) / VITESSE ** 2   # frottement en v^2

RESERVOIR = 40                 # litres (grand oral)


def conso_instantanee(vitesse, masse):
    """Consommation (L/s) à la vitesse (m/s) pour une masse (kg)."""
    base = CONSO_VOL + K_AIR * vitesse ** 2
    return base * masse / MASSE_SECHE


def distance_parcourue(volume, vitesse, dt=1.0):
    """Distance (m) faite avant la panne sèche, à vitesse constante."""
    if volume < 0 or vitesse <= 0:
        raise ValueError("volume et vitesse doivent etre positifs")
    temps = 0.0
    reste = volume
    while reste > 0:
        masse = MASSE_SECHE + RHO * reste
        reste = reste - conso_instantanee(vitesse, masse) * dt
        temps = temps + dt
    return vitesse * temps


def carburant_necessaire(vitesse, dt=1.0):
    """Volume (L) pour faire DISTANCE à cette vitesse (m/s)."""
    return dichotomie(lambda v: distance_parcourue(v, vitesse, dt) - DISTANCE,
                      0, 3000)


if __name__ == "__main__":
    # Test de validité : à 100 km/h on doit retrouver le résultat de jetpack.py
    a_100 = carburant_necessaire(VITESSE)
    print(f"A 100 km/h : {a_100:.1f} L")
    assert math.isclose(a_100, jetpack.carburant_necessaire(), rel_tol=1e-3)

    vitesses_kmh = list(range(50, 240, 5))
    volumes = [carburant_necessaire(v / 3.6) for v in vitesses_kmh]

    mini = min(volumes)
    meilleur = vitesses_kmh[volumes.index(mini)]    # à 5 km/h près
    print(f"Vitesse optimale : {meilleur} km/h -> {mini:.1f} L")
    print(f"Le réservoir fait {RESERVOIR} L : "
          f"{'suffisant' if mini <= RESERVOIR else 'INSUFFISANT'}")

    plt.figure()
    plt.plot(vitesses_kmh, volumes, label="carburant nécessaire")
    plt.axhline(RESERVOIR, color="red", linestyle="--",
                label=f"réservoir ({RESERVOIR} L)")
    plt.scatter([meilleur], [mini], color="green", zorder=3,
                label=f"optimum : {meilleur} km/h, {mini:.1f} L")
    plt.xlabel("vitesse de croisière (km/h)")
    plt.ylabel("carburant pour 30 km (L)")
    plt.title("Quelle vitesse de croisière consomme le moins ?\n"
              "(carburant nécessaire pour 30 km)")
    plt.legend()
    plt.savefig(os.path.join(DOSSIER, "vitesse_optimale.png"))
