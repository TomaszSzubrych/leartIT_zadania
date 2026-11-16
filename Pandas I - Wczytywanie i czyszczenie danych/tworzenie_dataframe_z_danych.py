import pandas as pd


# Dane 10 produktow sklepu
produkty = {
    "Nazwa": [
        "Laptop",
        "Mysz",
        "Klawiatura",
        "Monitor",
        "Sluchawki",
        "Smartfon",
        "Tablet",
        "Drukarka",
        "Kamera",
        "Glosnik"
    ],
    "Cena": [
        3500, 80, 250, 1200, 350,
        2200, 1500, 650, 900, 300
    ],
    "IloscNaStanie": [
        12, 80, 35, 18, 45,
        20, 15, 10, 8, 25
    ],
    "Kategoria": [
        "Komputery",
        "Akcesoria",
        "Akcesoria",
        "Monitory",
        "Audio",
        "Telefony",
        "Tablety",
        "Drukarki",
        "Akcesoria",
        "Audio"
    ]
}


# Utworzenie DataFrame ze slownika
df = pd.DataFrame(produkty)

# Dodanie kolumny z calkowita wartoscia towaru
df["WartośćCałkowita"] = df["Cena"] * df["IloscNaStanie"]


# Prezentacja wynikow
print("DATAFRAME - PRODUKTY SKLEPU")
print("=" * 65)

print("\nPierwsze 5 produktow:")
print(df.head())

print("\nPelna tabela produktow:")
print(df)

print("\nLiczba wierszy i kolumn:", df.shape)

print(
    "\nCalkowita wartosc towaru w magazynie:",
    f"{df['WartośćCałkowita'].sum():,.2f} PLN"
)
