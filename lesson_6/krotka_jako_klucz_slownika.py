
sprzedaz = {
    (2024, 'Q1'): 120_000,
    (2024, 'Q2'): 140_000,
    (2024, 'Q3'): 135_000,
    (2024, 'Q4'): 160_000
}

# 1. Odczyt sprzedaży za drugi kwartał
print("Sprzedaż Q2:", sprzedaz[(2024, 'Q2')])

# 2. Dodanie wpisu
sprzedaz[(2025, 'Q1')] = 130_000

# 3. Statystyki sprzedaży
wartosci = sprzedaz.values()

print("Najwyższa sprzedaż:", max(wartosci))
print("Najniższa sprzedaż:", min(wartosci))
print("Łączna sprzedaż:", sum(wartosci))

# 4. Liczba wpisów w słowniku
print("Liczba kwartałów:", len(sprzedaz))
