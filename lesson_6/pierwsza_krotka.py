
# 1. Utworzenie krotki
wymiary = (1920, 1080)

# 2. Rozpakowanie krotki
szerokosc, wysokosc = wymiary

print(f"Rozdzielczość: {szerokosc}x{wysokosc}")

# 3. Krotka jednoelementowa
samotny = (42,)
print("Krotka:", samotny)
print("Typ:", type(samotny))

# 4. Krotki nie można zmieniać
# samotny[0] = 100
# Błąd: TypeError — obiekt typu tuple nie obsługuje przypisania do elementu.

# 5. Utworzenie nowej krotki przez połączenie
nowa_krotka = samotny + (100, 200)
print("Nowa krotka:", nowa_krotka)
