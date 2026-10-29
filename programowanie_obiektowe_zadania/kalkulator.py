
class Kalkulator:
    def dodaj(self, a, b):
        return a + b

    def odejmij(self, a, b):
        return a - b

    def pomnoz(self, a, b):
        return a * b

    def podziel(self, a, b):
        if b == 0:
            return "Nie można dzielić przez zero."
        return a / b


kalkulator = Kalkulator()

print("Dodawanie:", kalkulator.dodaj(10, 5))
print("Odejmowanie:", kalkulator.odejmij(10, 5))
print("Mnożenie:", kalkulator.pomnoz(10, 5))
print("Dzielenie:", kalkulator.podziel(10, 5))
print("Dzielenie przez zero:", kalkulator.podziel(10, 0))
