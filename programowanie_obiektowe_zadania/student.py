
class Student:
    def __init__(self, imie, numer_indeksu, oceny=None):
        self.imie = imie
        self.numer_indeksu = numer_indeksu
        self.oceny = oceny if oceny is not None else []

    def dodaj_ocene(self, ocena):
        if 1 <= ocena <= 6:
            self.oceny.append(ocena)
        else:
            print("Ocena musi być w zakresie od 1 do 6.")

    def srednia(self):
        if not self.oceny:
            return 0
        return sum(self.oceny) / len(self.oceny)

    def __str__(self):
        return (
            f"Student: {self.imie}, indeks: {self.numer_indeksu}, "
            f"oceny: {self.oceny}"
        )


student1 = Student("Anna", 1001, [5, 4, 5])
student2 = Student("Jan", 1002, [3, 4, 4])
student3 = Student("Katarzyna", 1003)

student3.dodaj_ocene(6)
student3.dodaj_ocene(5)
student3.dodaj_ocene(6)

studenci = [student1, student2, student3]

for student in studenci:
    print(student)
    print(f"Średnia ocen: {student.srednia():.2f}")
    print()
