
dataset_a = {
    'wiek', 'plec', 'miasto', 'dochod',
    'wyksztalcenie', 'stan_cywilny'
}

dataset_b = {
    'wiek', 'plec', 'miasto', 'pensja',
    'stanowisko', 'staz'
}

# 1. Cechy wspólne
print("Cechy wspólne:", dataset_a & dataset_b)

# 2. Cechy tylko w dataset_a
print("Tylko w dataset_a:", dataset_a - dataset_b)

# 3. Cechy tylko w dataset_b
print("Tylko w dataset_b:", dataset_b - dataset_a)

# 4. Wszystkie unikalne cechy
print("Suma cech:", dataset_a | dataset_b)

# 5. Cechy występujące tylko w jednym datasecie
print("Różnica symetryczna:", dataset_a ^ dataset_b)

# 6. Sprawdzenie podzbioru
print(
    "Czy {'wiek', 'plec'} jest podzbiorem cech wspólnych:",
    {'wiek', 'plec'}.issubset(dataset_a & dataset_b)
)
