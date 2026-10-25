
produkty = [
    ("laptop", 2999, 4.5),
    ("mysz", 89, 4.2),
    ("klawiatura", 249, 4.8),
    ("monitor", 899, 4.3)
]

wedlug_ceny = sorted(produkty, key=lambda produkt: produkt[1])

wedlug_oceny = sorted(
    produkty,
    key=lambda produkt: produkt[2],
    reverse=True
)

print("Produkty według ceny rosnąco:")
for produkt in wedlug_ceny:
    print(produkt)

print("\nProdukty według oceny malejąco:")
for produkt in wedlug_oceny:
    print(produkt)
