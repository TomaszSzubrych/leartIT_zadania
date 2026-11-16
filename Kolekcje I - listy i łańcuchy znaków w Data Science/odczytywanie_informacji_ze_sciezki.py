filename = "model_results_2024_Q3.csv"

rok = filename[14:18]
kwartal = filename[19:21]
czy_csv = filename.endswith(".csv")

print(f"Plik: {filename}")
print(f"Rok: {rok}")
print(f"Kwartał: {kwartal}")
print(f"Czy plik ma rozszerzenie CSV? {czy_csv}")
