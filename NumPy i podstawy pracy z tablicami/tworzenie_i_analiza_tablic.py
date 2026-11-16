import numpy as np


# Tworzenie tablicy z liczbami od 1 do 100
numbers = np.arange(1, 101)

# Obliczanie podstawowych statystyk
total = np.sum(numbers)
average = np.mean(numbers)
median = np.median(numbers)
maximum = np.max(numbers)
minimum = np.min(numbers)

# Prezentacja wynikow
print("ANALIZA TABLICY NUMPY")
print("-" * 35)

print("Tablica:", numbers)
print("Suma elementow:", total)
print("Srednia arytmetyczna:", average)
print("Mediana:", median)
print("Wartosc maksymalna:", maximum)
print("Wartosc minimalna:", minimum)
