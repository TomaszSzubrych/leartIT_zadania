
grupa_a = {'python', 'pandas', 'numpy', 'sql', 'tableau'}
grupa_b = {'python', 'r', 'sql', 'ggplot2', 'dplyr'}

# SUMA — wszystkie narzędzia
print("Suma operator:", grupa_a | grupa_b)
print("Suma metoda:", grupa_a.union(grupa_b))

# ILOCZYN — elementy wspólne
print("Część wspólna operator:", grupa_a & grupa_b)
print("Część wspólna metoda:", grupa_a.intersection(grupa_b))

# RÓŻNICA — tylko w grupie A
print("Różnica operator:", grupa_a - grupa_b)
print("Różnica metoda:", grupa_a.difference(grupa_b))

# RÓŻNICA SYMETRYCZNA — tylko w jednej grupie
print("Różnica symetryczna operator:", grupa_a ^ grupa_b)
print("Różnica symetryczna metoda:",
      grupa_a.symmetric_difference(grupa_b))

# Sprawdzenie rozłączności
print("Czy zbiory są rozłączne:", grupa_a.isdisjoint(grupa_b))
