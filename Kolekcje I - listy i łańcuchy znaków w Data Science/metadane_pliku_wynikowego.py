sciezka = "/data/processed/2024/experiment_42_v3.csv"
elementy_sciezki = sciezka.split("/")

nazwa_pliku = elementy_sciezki[-1]
katalog = "/" + "/".join(elementy_sciezki[1:-1])
nazwa_bez_rozszerzenia = nazwa_pliku[:-4]
rozszerzenie = nazwa_pliku[-4:]
rok = elementy_sciezki[-2]

print("Informacje o pliku")
print("-" * 42)
print(f"{'Nazwa pliku:':<25}{nazwa_pliku}")
print(f"{'Katalog:':<25}{katalog}")
print(f"{'Nazwa bez rozszerzenia:':<25}{nazwa_bez_rozszerzenia}")
print(f"{'Rozszerzenie:':<25}{rozszerzenie}")
print(f"{'Rok:':<25}{rok}")
