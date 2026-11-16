import numpy as np


# Oceny studentow
grades = np.array([78, 45, 92, 67, 34, 88, 56, 91, 23, 85, 73, 95])

# Wybieranie ocen wysokich
high_grades = grades[grades >= 80]

# Wybieranie ocen niedostatecznych
low_grades = grades[grades < 50]

# Zliczanie ocen z przedzialu [60, 80)
medium_count = np.sum((grades >= 60) & (grades < 80))

# Kopia tablicy i podniesienie ocen ponizej 50
adjusted_grades = grades.copy()
adjusted_grades[adjusted_grades < 50] = 50

# Prezentacja wynikow
print("BOOLEAN INDEXING - ANALIZA OCEN")
print("-" * 40)

print("Oryginalne oceny:", grades)
print("Oceny wysokie (>= 80):", high_grades)
print("Oceny niedostateczne (< 50):", low_grades)
print("Liczba ocen w przedziale [60, 80):", medium_count)
print("Oceny po podniesieniu minimum do 50:", adjusted_grades)
