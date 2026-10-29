
class Zadanie:
    def __init__(self, opis, status="do zrobienia"):
        self.opis = opis
        self.status = status

    def oznacz_jako_zrobione(self):
        self.status = "zrobione"

    def __str__(self):
        return f"{self.opis} - status: {self.status}"


zadania = [
    Zadanie("Nauczyć się klas"),
    Zadanie("Napisać program"),
    Zadanie("Przetestować kod"),
    Zadanie("Przeczytać dokumentację"),
    Zadanie("Wysłać projekt na GitHub"),
]

zadania[0].oznacz_jako_zrobione()
zadania[2].oznacz_jako_zrobione()
zadania[4].oznacz_jako_zrobione()

for zadanie in zadania:
    print(zadanie)
