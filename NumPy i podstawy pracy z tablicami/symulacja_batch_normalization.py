import numpy as np


# Przygotowanie mini-batch: 32 probki i 10 cech
np.random.seed(8)
batch = np.random.randn(32, 10) * 5 + 20

# Obliczenie statystyk per cecha
mean = np.mean(batch, axis=0)
std = np.std(batch, axis=0)

# Standaryzacja danych
batch_norm = (batch - mean) / std

# Parametry scale i shift
gamma = 2.0
beta = 1.0

# Zastosowanie transformacji z wykorzystaniem broadcastingu
output = gamma * batch_norm + beta


# Funkcja prezentujaca statystyki
def print_statistics(data, title):
    print(f"\n{title}")
    print("-" * 45)
    print("Mean per cecha:")
    print(np.round(np.mean(data, axis=0), 4))
    print("Std per cecha:")
    print(np.round(np.std(data, axis=0), 4))


# Funkcja generujaca histogram tekstowy
def print_histogram(values, title, bins=10):
    counts, edges = np.histogram(values, bins=bins)

    print(f"\n{title}")
    print("-" * 45)

    for i in range(len(counts)):
        bar = "█" * counts[i]
        print(
            f"{edges[i]:8.2f} - {edges[i + 1]:8.2f} | "
            f"{bar} ({counts[i]})"
        )


# Prezentacja wynikow
print("SYMULACJA BATCH NORMALIZATION")
print("=" * 45)

print("Ksztalt batch:", batch.shape)
print("Gamma:", gamma)
print("Beta:", beta)

print_statistics(batch, "STATYSTYKI PRZED NORMALIZACJA")
print_statistics(batch_norm, "STATYSTYKI PO NORMALIZACJI")
print_statistics(output, "STATYSTYKI PO SCALE I SHIFT")

# Histogram pierwszej cechy przed i po transformacji
print_histogram(batch[:, 0], "HISTOGRAM CECHY 0 - PRZED NORMALIZACJA")
print_histogram(output[:, 0], "HISTOGRAM CECHY 0 - PO SCALE I SHIFT")

print("\nPierwsze 5 probek po transformacji:")
print(np.round(output[:5], 3))
