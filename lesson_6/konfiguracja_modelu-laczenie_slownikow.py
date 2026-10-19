
domyslne = {
    'lr': 0.01,
    'epochs': 100,
    'optimizer': 'sgd',
    'batch_size': 32
}

uzytkownika = {
    'lr': 0.001,
    'batch_size': 64,
    'momentum': 0.9
}

# 1. Łączenie słowników operatorem |
finalna_1 = domyslne | uzytkownika

# 2. Łączenie za pomocą update() i copy()
finalna_2 = domyslne.copy()
finalna_2.update(uzytkownika)

# 3. Porównanie słowników
print("Czy konfiguracje są równe:", finalna_1 == finalna_2)

# 4. Wyświetlenie wybranych parametrów
print(
    f"lr: {finalna_1['lr']}\n"
    f"batch_size: {finalna_1['batch_size']}\n"
    f"momentum: {finalna_1['momentum']}"
)
