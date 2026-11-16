import numpy as np


# Ceny produktow przed i po rabacie
before = np.array([100, 250, 75, 320, 180, 450, 90])
after = np.array([80, 200, 60, 280, 150, 400, 75])

# Obliczanie oszczednosci dla kazdego produktu
savings = before - after

# Obliczanie procentu rabatu
discount_percent = (savings / before) * 100

# Obliczanie sredniej oszczednosci
average_saving = np.mean(savings)

# Prezentacja wynikow
print("ANALIZA RABATOW PRODUKTOW")
print("-" * 40)

print("Ceny przed rabatem:", before)
print("Ceny po rabacie:   ", after)
print("Oszczednosci:      ", savings)
print("Procent rabatu:    ", np.round(discount_percent, 2), "%")
print("Srednia oszczednosc:", round(average_saving, 2))
