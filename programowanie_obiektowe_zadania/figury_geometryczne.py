
import math


class Figura:
    def pole(self):
        raise NotImplementedError(
            "Każda figura musi implementować metodę pole()."
        )


class Prostokat(Figura):
    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

    def pole(self):
        return self.szerokosc * self.wysokosc


class Kolo(Figura):
    def __init__(self, promien):
        self.promien = promien

    def pole(self):
        return math.pi * self.promien ** 2


figury = [
    Prostokat(4, 5),
    Kolo(3),
    Prostokat(2, 8),
    Kolo(2),
]

laczne_pole = 0

for figura in figury:
    pole_figury = figura.pole()
    laczne_pole += pole_figury
    print(f"Pole figury: {pole_figury:.2f}")

print(f"\nŁączne pole wszystkich figur: {laczne_pole:.2f}")
