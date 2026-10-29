
class Uczen:
    def __init__(self, imie, oceny=None):
        self.imie = imie
        self.oceny = oceny if oceny is not None else []

    def srednia(self):
        if not self.oceny:
            return 0
        return sum(self.oceny) / len(self.oceny)


class Klasa:
    def __init__(self, nazwa, uczniowie=None):
        self.nazwa = nazwa
        self.uczniowie = uczniowie if uczniowie is not None else []

    def dodaj_ucznia(self, uczen):
        self.uczniowie.append(uczen)

    def srednia_klasy(self):
        wszyscy_uczniowie = [
            uczen for uczen in self.uczniowie if uczen.oceny
        ]

        if not wszyscy_uczniowie:
            return 0

        suma_srednich = sum(
            uczen.srednia() for uczen in wszyscy_uczniowie
        )

        return suma_srednich / len(wszyscy_uczniowie)

    def najlepszy_uczen(self):
        uczniowie_z_ocenami = [
            uczen for uczen in self.uczniowie if uczen.oceny
        ]

        if not uczniowie_z_ocenami:
            return None

        return max(uczniowie_z_ocenami, key=lambda uczen: uczen.srednia())


klasa = Klasa("3A")

klasa.dodaj_ucznia(Uczen("Anna", [5, 5, 4, 6]))
klasa.dodaj_ucznia(Uczen("Jan", [3, 4, 4, 3]))
klasa.dodaj_ucznia(Uczen("Katarzyna", [6, 6, 5, 6]))
klasa.dodaj_ucznia(Uczen("Piotr", [4, 4, 5, 3]))
klasa.dodaj_ucznia(Uczen("Marek", [5, 4, 5, 5]))

print(f"Klasa: {klasa.nazwa}")
print(f"Średnia klasy: {klasa.srednia_klasy():.2f}")

najlepszy = klasa.najlepszy_uczen()

if najlepszy is not None:
    print(f"Najlepszy uczeń: {najlepszy.imie}")
    print(f"Średnia najlepszego ucznia: {najlepszy.srednia():.2f}")

print("\nŚrednie poszczególnych uczniów:")

for uczen in klasa.uczniowie:
    print(f"{uczen.imie}: {uczen.srednia():.2f}")
