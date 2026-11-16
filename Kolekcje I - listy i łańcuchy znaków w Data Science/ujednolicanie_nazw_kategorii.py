kat_a = "   Electronics       "
kat_b = "ELECTRONICS"

kat_a_norm = kat_a.strip().lower()
kat_b_norm = kat_b.strip().lower()

czy_kategorie_sa_zgodne = kat_a_norm == kat_b_norm

print(f"Kategoria A przed zmianą: '{kat_a}'")
print(f"Kategoria B przed zmianą: '{kat_b}'")
print(f"Kategoria A po zmianie:   '{kat_a_norm}'")
print(f"Kategoria B po zmianie:   '{kat_b_norm}'")
print(f"Czy kategorie są takie same? {czy_kategorie_sa_zgodne}")
