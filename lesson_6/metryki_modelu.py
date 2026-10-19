
metryki = {
    'accuracy': 0.94,
    'precision': 0.91,
    'recall': 0.89,
    'f1_score': 0.90
}

# Pobranie wartości metryk
wartosci = list(metryki.values())

# Najwyższa i najniższa metryka
print("Najwyższa metryka:", max(wartosci))
print("Najniższa metryka:", min(wartosci))

# Średnia metryka z dokładnością do 3 miejsc po przecinku
srednia = sum(wartosci) / len(wartosci)
print(f"Średnia metryka: {srednia:.3f}")

# Klucze posortowane alfabetycznie
print("Klucze alfabetycznie:", sorted(metryki.keys()))

# Wartości posortowane rosnąco
print("Wartości rosnąco:", sorted(wartosci))
