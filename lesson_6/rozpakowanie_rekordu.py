
pracownik = ('Julia', 'Wiśniewska', 28, 'Data Analyst', 8500.0)

# 1. Rozpakowanie wszystkich pól
imie, nazwisko, wiek, stanowisko, pensja = pracownik

# 2. Formatowanie wyniku
print(f"{imie} {nazwisko} ({wiek}) – {stanowisko}, pensja: {pensja:.2f} zł")

# 3. Rozpakowanie z gwiazdką
imie, *reszta = pracownik

print("Imię:", imie)
print("Reszta:", reszta)
