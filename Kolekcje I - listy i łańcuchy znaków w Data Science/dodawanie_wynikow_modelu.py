# Wyniki accuracy z kolejnych prób modelu
results = []

results.append(0.75)
results.append(0.82)
results.append(0.79)
results.append(0.85)
results.append(0.88)

srednia = sum(results) / len(results)

print(f"Wyniki: {results}")
print(f"Liczba wyników: {len(results)}")
print(f"Średnia accuracy: {srednia:.2%}")
print(f"Najlepszy wynik: {max(results):.2%}")
print(f"Najsłabszy wynik: {min(results):.2%}")
