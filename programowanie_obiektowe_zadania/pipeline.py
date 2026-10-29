
class FiltrowanieDodatnich:
    def przetworz(self, dane):
        return [liczba for liczba in dane if liczba >= 0]


class Zaokraglanie:
    def przetworz(self, dane):
        return [round(liczba) for liczba in dane]


class Skalowanie:
    def __init__(self, wspolczynnik):
        self.wspolczynnik = wspolczynnik

    def przetworz(self, dane):
        return [liczba * self.wspolczynnik for liczba in dane]


class Sumowanie:
    def przetworz(self, dane):
        return sum(dane)


class Pipeline:
    def __init__(self, kroki):
        self.kroki = kroki

    def wykonaj(self, dane):
        wynik = dane

        for krok in self.kroki:
            wynik = krok.przetworz(wynik)

        return wynik


dane = [1.7, -3.2, 5.8, -1.1, 8.3, 2.4]

pipeline = Pipeline([
    FiltrowanieDodatnich(),
    Zaokraglanie(),
    Skalowanie(2),
    Sumowanie(),
])

wynik = pipeline.wykonaj(dane)

print("Dane początkowe:", dane)
print("Wynik pipeline:", wynik)
