
konfig = {
    'lr': 0.01,
    'epochs': 100,
    'optimizer': 'adam'
}

# Pobranie istniejącego klucza
print("lr:", konfig.get('lr'))

# Pobranie nieistniejącego klucza
print("momentum:", konfig.get('momentum'))

# Pobranie nieistniejącego klucza z wartością domyślną
print("momentum z wartością domyślną:", konfig.get('momentum', 0.9))

# Sprawdzenie, czy klucz istnieje
print("Czy istnieje batch_size:", 'batch_size' in konfig)
