"""Partie 4 : le bruit. À quelle distance, et pour combien de jetpacks,
le bruit reste-t-il supportable ?

Modèle (HYPOTHÈSES) : 120 dB à 1 m pour un jetpack, N jetpacks identiques
au même endroit, propagation libre sans absorption (-6 dB à chaque
doublement de la distance).
"""

import math
import os
import matplotlib.pyplot as plt

DOSSIER = os.path.dirname(os.path.abspath(__file__))

NIVEAU_REF = 120        # dB (grand oral)
DIST_REF = 1.0          # m : distance de la mesure (HYPOTHÈSE)
SEUIL_AUDITIF = 85      # dB : risque pour l'ouïe
SEUIL_CONFORT = 55      # dB : calme en extérieur en journée


def niveau(n, distance):
    """Niveau sonore (dB) de n jetpacks à la distance (m)."""
    if n < 1 or distance <= 0:
        raise ValueError("n >= 1 et distance > 0")
    return (NIVEAU_REF + 10 * math.log10(n)
            - 20 * math.log10(distance / DIST_REF))


def distance_pour_seuil(n, seuil):
    """Distance (m) à partir de laquelle n jetpacks passent sous seuil dB."""
    if n < 1:
        raise ValueError("n >= 1")
    return DIST_REF * 10 ** ((NIVEAU_REF + 10 * math.log10(n) - seuil) / 20)


if __name__ == "__main__":
    for n in [1, 2, 10, 100]:
        d1 = distance_pour_seuil(n, SEUIL_AUDITIF)
        d2 = distance_pour_seuil(n, SEUIL_CONFORT)
        print(f"N = {n:>3} : {niveau(n, 1):.0f} dB à 1 m, "
              f"< 85 dB à {d1:.0f} m, < 55 dB à {d2:.0f} m")

    # Vérification par une propriété : on retombe bien sur le seuil
    assert math.isclose(niveau(10, distance_pour_seuil(10, 85)), 85)

    distances = [10 ** (i / 20) for i in range(0, 101)]    # 1 m à 100 km
    plt.figure()
    for n in [1, 10, 100]:
        nom = f"{n} jetpack" + ("s" if n > 1 else "")
        courbe, = plt.plot(distances, [niveau(n, d) for d in distances],
                           label=nom)
        # points où la courbe franchit les deux seuils (valeurs du tableau)
        plt.scatter([distance_pour_seuil(n, SEUIL_AUDITIF),
                     distance_pour_seuil(n, SEUIL_CONFORT)],
                    [SEUIL_AUDITIF, SEUIL_CONFORT],
                    color=courbe.get_color(), zorder=3)
    plt.axhline(SEUIL_AUDITIF, color="red", linestyle="--",
                label="risque auditif (85 dB)")
    plt.axhline(SEUIL_CONFORT, color="green", linestyle="--",
                label="calme (55 dB)")
    plt.xscale("log")
    plt.xlabel("distance au(x) jetpack(s) (m)")
    plt.ylabel("niveau sonore (dB)")
    plt.title("Niveau sonore selon la distance, pour N jetpacks identiques\n"
              "(propagation libre, les points marquent les seuils franchis)")
    plt.legend()
    plt.savefig(os.path.join(DOSSIER, "bruit.png"))
