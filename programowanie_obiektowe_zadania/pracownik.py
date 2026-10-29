
class Pracownik:
    def __init__(self, imie, stanowisko, pensja):
        self.imie = imie
        self.stanowisko = stanowisko
        self.pensja = pensja

    def podwyzka(self, procent):
        if procent < 0:
            print("Procent podwyżki nie może być ujemny.")
        else:
            self.pensja *= 1 + procent / 100

    def __str__(self):
        return (
            f"{self.imie} - {self.stanowisko}, "
            f"pensja: {self.pensja:.2f} zł"
        )


pracownik1 = Pracownik("Anna", "Programistka", 7000)
pracownik2 = Pracownik("Jan", "Tester", 6000)
pracownik3 = Pracownik("Piotr", "Administrator", 6500)

pracownik1.podwyzka(10)
pracownik2.podwyzka(5)
pracownik3.podwyzka(8)

print(pracownik1)
print(pracownik2)
print(pracownik3)
