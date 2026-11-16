modele = ["LogisticRegression", "RandomForest", "XGBoost", "SVM"]

lista_modeli = ", ".join(modele)
zapytanie = f"SELECT model FROM ({lista_modeli})"

modele_po_podziale = lista_modeli.split(", ")
czy_lista_jest_taka_sama = modele_po_podziale == modele

print(f"Połączone nazwy: {lista_modeli}")
print(f"Zapytanie SQL: {zapytanie}")
print(f"Lista po ponownym podziale: {modele_po_podziale}")
print(f"Czy otrzymaliśmy pierwotną listę? {czy_lista_jest_taka_sama}")
