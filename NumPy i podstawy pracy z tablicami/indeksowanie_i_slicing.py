import numpy as np


# Temperatury z kolejnych dni
temps = np.array([15, 18, 22, 25, 23, 20, 17, 14, 16, 19, 21, 24])

# Temperatury z dni o indeksach parzystych
even_days = temps[::2]

# Ostatnie 5 temperatur
last_five = temps[-5:]

# Temperatury w odwrotnej kolejnosci
reversed_temps = temps[::-1]

# Temperatury wyzsze niz 20
above_twenty = temps[temps > 20]

# Prezentacja wynikow
print("INDEKSOWANIE I SLICING W NUMPY")
print("-" * 40)

print("Oryginalna tablica:", temps)
print("Temperatury z dni o indeksach parzystych:", even_days)
print("Ostatnie 5 temperatur:", last_five)
print("Temperatury w odwrotnej kolejnosci:", reversed_temps)
print("Temperatury wieksze niz 20:", above_twenty)
