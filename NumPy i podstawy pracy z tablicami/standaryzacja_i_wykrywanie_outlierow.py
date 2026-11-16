import numpy as np


# Przygotowanie danych: 100 wartosci normalnych i 5 outlierow
np.random.seed(42)
data = np.concatenate([
    np.random.randn(100) * 10 + 50,
    np.array([150, -50, 200, -100, 180])
])

np.random.shuffle(data)

# Standaryzacja danych metoda z-score
mean_before = np.mean(data)
std_before = np.std(data)
z_scores = (data - mean_before) / std_before

# Wykrywanie wartosci odstajacych
outlier_mask = np.abs(z_scores) > 3
outliers = data[outlier_mask]

# Usuniecie outlierow
clean_data = data[~outlier_mask]

# Ponowna standaryzacja oczyszczonych danych
mean_after = np.mean(clean_data)
std_after = np.std(clean_data)
normalized_clean_data = (clean_data - mean_after) / std_after


# Funkcja prezentujaca statystyki zbioru
def print_statistics(values, title):
    print(f"\n{title}")
    print("-" * 40)
    print("Mean:", round(np.mean(values), 4))
    print("Std:", round(np.std(values), 4))
    print("Min:", round(np.min(values), 4))
    print("Max:", round(np.max(values), 4))
    print("Liczba elementow:", len(values))


# Funkcja generujaca histogram tekstowy
def print_histogram(values, title, bins=10):
    counts, edges = np.histogram(values, bins=bins)

    print(f"\n{title}")
    print("-" * 40)

    for i in range(len(counts)):
        bar = "█" * counts[i]
        print(
            f"{edges[i]:8.2f} - {edges[i + 1]:8.2f} | "
            f"{bar} ({counts[i]})"
        )


# Prezentacja wynikow
print("STANDARYZACJA I WYKRYWANIE OUTLIEROW")
print("=" * 45)

print_statistics(data, "STATYSTYKI PRZED USUNIECIEM OUTLIEROW")

print("\nWykryte wartosci odstajace:")
print(np.round(outliers, 4))
print("Liczba wykrytych outlierow:", len(outliers))

print_statistics(clean_data, "STATYSTYKI PO USUNIECIU OUTLIEROW")

print("\nStatystyki ponownie standaryzowanych danych:")
print("Mean:", round(np.mean(normalized_clean_data), 4))
print("Std:", round(np.std(normalized_clean_data), 4))

print_histogram(data, "HISTOGRAM PRZED USUNIECIEM OUTLIEROW")
print_histogram(clean_data, "HISTOGRAM PO USUNIECIU OUTLIEROW")
