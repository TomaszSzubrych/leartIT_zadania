
class Pojazd:
    def __init__(self, marka, model, rok):
        self.marka = marka
        self.model = model
        self.rok = rok

    def pokaz_info(self):
        print(f"Marka: {self.marka}")
        print(f"Model: {self.model}")
        print(f"Rok produkcji: {self.rok}")


class Samochod(Pojazd):
    def __init__(self, marka, model, rok, liczba_drzwi):
        super().__init__(marka, model, rok)
        self.liczba_drzwi = liczba_drzwi

    def pokaz_info(self):
        super().pokaz_info()
        print(f"Liczba drzwi: {self.liczba_drzwi}")


samochod = Samochod("Toyota", "Corolla", 2022, 5)
samochod.pokaz_info()
