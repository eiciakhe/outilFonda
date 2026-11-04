"""Partie 5 : le duel. Jetpack contre le transport habituel, sur 30 km."""

from jetpack import DISTANCE
from vitesse import carburant_necessaire, RESERVOIR


TRANSPORT_NOM = "voiture"
TRANSPORT_MIN = 30           # minutes de trajet (HYPOTHÈSE)
TRANSPORT_EURO = 7           # prix du trajet (HYPOTHÈSE)

PRIX_LITRE = 80 / 40         # 2 EUR/L, d'après le grand oral


def duel(vitesse_kmh):
    """Temps (min), carburant (L) et coût (EUR) du jetpack à cette vitesse."""
    temps = DISTANCE / (vitesse_kmh / 3.6) / 60
    litres = carburant_necessaire(vitesse_kmh / 3.6)
    return temps, litres, litres * PRIX_LITRE


if __name__ == "__main__":
    print(f"{'':<22}{'temps':>10}{'carburant':>12}{'coût':>10}")
    print(f"{TRANSPORT_NOM:<22}{TRANSPORT_MIN:>7.0f} min{'-':>12}"
          f"{TRANSPORT_EURO:>8.2f} EUR")
    for vitesse in [100, 140, 235]:
        temps, litres, cout = duel(vitesse)
        print(f"jetpack {vitesse:>3} km/h".ljust(22)
              + f"{temps:>7.1f} min{litres:>10.1f} L{cout:>8.2f} EUR")
        if litres > RESERVOIR:
            print(f"   -> impossible : {litres:.0f} L > réservoir de {RESERVOIR} L")
