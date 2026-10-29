
class BankAccount:
    def __init__(self, wlasciciel, saldo=0):
        self.wlasciciel = wlasciciel
        self.saldo = saldo

    def wplac(self, kwota):
        if kwota <= 0:
            print("Kwota wpłaty musi być większa od zera.")
        else:
            self.saldo += kwota
            print(f"Wpłacono {kwota:.2f} zł.")

    def wyplac(self, kwota):
        if kwota <= 0:
            print("Kwota wypłaty musi być większa od zera.")
        elif kwota > self.saldo:
            print("Brak wystarczających środków.")
        else:
            self.saldo -= kwota
            print(f"Wypłacono {kwota:.2f} zł.")

    def pokaz_saldo(self):
        print(f"Właściciel: {self.wlasciciel}")
        print(f"Saldo: {self.saldo:.2f} zł")


konto1 = BankAccount("Anna", 1000)
konto2 = BankAccount("Jan", 500)
konto3 = BankAccount("Piotr")

konto1.wplac(200)
konto1.wyplac(150)
konto1.pokaz_saldo()

print()

konto2.wyplac(700)
konto2.pokaz_saldo()

print()

konto3.wplac(300)
konto3.pokaz_saldo()
