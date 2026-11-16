import numpy as np


# Sprzedaz 6 produktow w ciagu 28 dni
np.random.seed(3)
sales = np.random.randint(50, 200, size=(6, 28))

# Trend sprzedazy: ostatnie 7 dni minus pierwsze 7 dni
first_week = np.sum(sales[:, :7], axis=1)
last_week = np.sum(sales[:, -7:], axis=1)
sales_trend = last_week - first_week

# Suma sprzedazy w kazdym z czterech tygodni
week_1 = np.sum(sales[:, 0:7])
week_2 = np.sum(sales[:, 7:14])
week_3 = np.sum(sales[:, 14:21])
week_4 = np.sum(sales[:, 21:28])

weekly_totals = np.array([week_1, week_2, week_3, week_4])

# Najlepszy tydzien
best_week = np.argmax(weekly_totals)

# Laczna sprzedaz kazdego produktu
product_totals = np.sum(sales, axis=1)

# Prezentacja wynikow
print("ANALIZA DATASETU SPRZEDAZY")
print("-" * 45)

print("\nMacierz sprzedazy (produkty x dni):")
print(sales)

print("\nTrend sprzedazy per produkt:")
print(sales_trend)

print("\nLaczna sprzedaz w poszczegolnych tygodniach:")
print(weekly_totals)

print("\nNajlepszy tydzien:", best_week)
print("Laczna sprzedaz najlepszego tygodnia:", weekly_totals[best_week])

print("\nLaczna sprzedaz per produkt:")
print(product_totals)

print("\nWYKRES SLUPKOWY SPRZEDAZY")
print("(jeden znak █ = 100 sztuk)")

for i in range(len(product_totals)):
    bar = "█" * (product_totals[i] // 100)
    print(f"Produkt {i + 1}: {bar} ({product_totals[i]})")
