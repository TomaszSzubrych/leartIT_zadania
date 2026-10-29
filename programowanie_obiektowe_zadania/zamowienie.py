
class Produkt:
    def __init__(self, nazwa, cena):
        self.nazwa = nazwa
        self.cena = cena


class Zamowienie:
    def __init__(self):
        self.produkty = []

    def dodaj_produkt(self, produkt, ilosc):
        if ilosc <= 0:
            print("Ilość musi być większa od zera.")
            return

        self.produkty.append((produkt, ilosc))

    def laczna_wartosc(self):
        return sum(
            produkt.cena * ilosc
            for produkt, ilosc in self.produkty
        )

    def pokaz_zamowienie(self):
        print("ZAMÓWIENIE")
        print("-" * 40)

        for produkt, ilosc in self.produkty:
            wartosc = produkt.cena * ilosc
            print(
                f"{produkt.nazwa}: {ilosc} szt. x "
                f"{produkt.cena:.2f} zł = {wartosc:.2f} zł"
            )

        print("-" * 40)
        print(f"Łączna wartość: {self.laczna_wartosc():.2f} zł")


produkt1 = Produkt("Laptop", 3500)
produkt2 = Produkt("Mysz", 80)
produkt3 = Produkt("Klawiatura", 150)
produkt4 = Produkt("Monitor", 900)
produkt5 = Produkt("Słuchawki", 200)

zamowienie = Zamowienie()

zamowienie.dodaj_produkt(produkt1, 1)
zamowienie.dodaj_produkt(produkt2, 2)
zamowienie.dodaj_produkt(produkt3, 1)
zamowienie.dodaj_produkt(produkt4, 2)
zamowienie.dodaj_produkt(produkt5, 1)

zamowienie.pokaz_zamowienie()
