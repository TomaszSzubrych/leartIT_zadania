import numpy as np


# Przygotowanie danych sprzedazowych
np.random.seed(1)
sales = np.random.randint(10, 100, size=(4, 7))

# Srednia sprzedaz kazdego produktu
average_per_product = np.mean(sales, axis=1)

# Srednia sprzedaz kazdego dnia
average_per_day = np.mean(sales, axis=0)

# Suma sprzedazy w kazdym dniu
daily_totals = np.sum(sales, axis=0)

# Indeks dnia z najwyzsza laczna sprzedaza
best_day = np.argmax(daily_totals)

# Indeks produktu z najnizsza srednia sprzedaza
lowest_product = np.argmin(average_per_product)

# Prezentacja wynikow
print("ANALIZA SPRZEDAZY PRODUKTOW")
print("-" * 40)

print("Macierz sprzedazy (produkty x dni):")
print(sales)

print("\nSrednia sprzedaz per produkt:", np.round(average_per_product, 2))
print("Srednia sprzedaz per dzien:", np.round(average_per_day, 2))

print("\nLaczna sprzedaz per dzien:", daily_totals)
print("Dzien z najwyzsza laczna sprzedaza:", best_day + 1)
print("Wartosc najwyzszej sprzedazy:", daily_totals[best_day])

print("\nProdukt z najnizsza srednia sprzedaza:", lowest_product + 1)
print("Najnisza srednia sprzedaz:", round(average_per_product[lowest_product], 2))
