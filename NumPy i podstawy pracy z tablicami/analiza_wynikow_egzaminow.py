import numpy as np


# Wyniki egzaminow: 5 studentow i 4 egzaminy
exams = np.array([
    [78, 85, 92, 88],
    [65, 72, 68, 70],
    [90, 88, 95, 92],
    [55, 60, 58, 62],
    [82, 79, 85, 80]
])

# Punkty bonusowe dla kazdego egzaminu
bonus = np.array([5, 10, 5, 10])

# Indywidualne mnozniki dla studentow
multipliers = np.array([1.0, 1.1, 0.95, 1.15, 1.0])

# Dodanie punktow bonusowych z wykorzystaniem broadcastingu
bonus_scores = exams + bonus

# Zastosowanie mnoznikow dla poszczegolnych studentow
final_scores = bonus_scores * multipliers[:, np.newaxis]

# Prezentacja wynikow
print("ANALIZA WYNIKOW EGZAMINOW")
print("-" * 40)

print("\nWyniki poczatkowe:")
print(exams)

print("\nPunkty bonusowe:")
print(bonus)

print("\nWyniki po dodaniu bonusow:")
print(bonus_scores)

print("\nMnozniki studentow:")
print(multipliers)

print("\nWyniki koncowe po zastosowaniu mnoznikow:")
print(np.round(final_scores, 2))
