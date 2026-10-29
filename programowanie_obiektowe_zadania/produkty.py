
class Produkt:
    def __init__(self, nazwa, cena, ilosc_w_magazynie):
        self.nazwa = nazwa
        self.cena = cena
        self.ilosc_w_magazynie = ilosc_w_magazynie

    def pokaz_info(self):
        print(f"Nazwa: {self.nazwa}")
        print(f"Cena: {self.cena:.2f} zł")
        print(f"Ilość w magazynie: {self.ilosc_w_magazynie}")

    def sprzedaj(self, ilosc):
        if ilosc <= 0:
            print("Ilość musi być większa od zera.")
        elif ilosc > self.ilosc_w_magazynie:
            print("Brak wystarczającej ilości w magazynie.")
        else:
            self.ilosc_w_magazynie -= ilosc
            print(f"Sprzedano {ilosc} szt. produktu: {self.nazwa}")

    def dostawa(self, ilosc):
        if ilosc <= 0:
            print("Ilość musi być większa od zera.")
        else:
            self.ilosc_w_magazynie += ilosc
            print(f"Przyjęto dostawę: {ilosc} szt. produktu {self.nazwa}")


produkt1 = Produkt("Laptop", 3500, 10)
produkt2 = Produkt("Mysz", 80, 25)
produkt3 = Produkt("Klawiatura", 150, 15)

produkt1.pokaz_info()
print()

produkt2.sprzedaj(3)
produkt2.pokaz_info()
print()

produkt3.dostawa(5)
produkt3.pokaz_info()
