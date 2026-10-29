
class Ksiazka:
    def __init__(self, tytul, autor, rok_wydania, liczba_stron):
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
        self.liczba_stron = liczba_stron

    def __str__(self):
        return (
            f"'{self.tytul}' - autor: {self.autor}, "
            f"rok wydania: {self.rok_wydania}, "
            f"liczba stron: {self.liczba_stron}"
        )


ksiazki = [
    Ksiazka("Wiedźmin", "Andrzej Sapkowski", 1990, 288),
    Ksiazka("Lalka", "Bolesław Prus", 1890, 720),
    Ksiazka("Hobbit", "J.R.R. Tolkien", 1937, 320),
    Ksiazka("Harry Potter", "J.K. Rowling", 1997, 320),
    Ksiazka("Solaris", "Stanisław Lem", 1961, 300),
]

for ksiazka in ksiazki:
    print(ksiazka)
