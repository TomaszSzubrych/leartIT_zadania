import numpy as np


# Przygotowanie ocen studentow
np.random.seed(2)
scores = np.random.randint(40, 100, size=(20, 3))

# Normalizacja Min-Max per przedmiot
minimum = np.min(scores, axis=0)
maximum = np.max(scores, axis=0)
normalized_scores = (scores - minimum) / (maximum - minimum)

# Sprawdzenie zakresu po normalizacji
normalized_minimum = np.min(normalized_scores, axis=0)
normalized_maximum = np.max(normalized_scores, axis=0)

# Histogram tekstowy
def print_histogram(data, title, bins=10):
    counts, edges = np.histogram(data, bins=bins)

    print(f"\n{title}")
    for i in range(len(counts)):
        bar = "█" * counts[i]
        print(f"{edges[i]:6.2f} - {edges[i + 1]:6.2f} | {bar} ({counts[i]})")


# Prezentacja wynikow
print("NORMALIZACJA DANYCH METODA MIN-MAX")
print("-" * 45)

print("\nOceny przed normalizacja:")
print(scores)

print("\nOceny po normalizacji:")
print(np.round(normalized_scores, 3))

print("\nMinimum kolumn po normalizacji:")
print(normalized_minimum)

print("\nMaksimum kolumn po normalizacji:")
print(normalized_maximum)

print_histogram(scores, "HISTOGRAM PRZED NORMALIZACJA")
print_histogram(normalized_scores, "HISTOGRAM PO NORMALIZACJI")
