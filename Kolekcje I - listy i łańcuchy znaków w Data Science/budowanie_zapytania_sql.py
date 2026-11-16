tabela = "customers"
kolumny = ["id", "name", "email", "city"]
warunek = "city = 'New York'"

lista_kolumn = ", ".join(kolumny)
zapytanie = f"SELECT {lista_kolumn} FROM {tabela} WHERE {warunek}"

print(zapytanie)
