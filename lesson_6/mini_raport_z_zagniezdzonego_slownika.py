
raport = {
    'Q1': {'przychod': 120_000, 'koszt': 80_000},
    'Q2': {'przychod': 145_000, 'koszt': 92_000},
    'Q3': {'przychod': 138_000, 'koszt': 88_000},
    'Q4': {'przychod': 167_000, 'koszt': 101_000}
}

# 1. Przychody poszczególnych kwartałów — bez pętli
print("Przychody:")
print("Q1:", raport['Q1']['przychod'])
print("Q2:", raport['Q2']['przychod'])
print("Q3:", raport['Q3']['przychod'])
print("Q4:", raport['Q4']['przychod'])

# 2. Obliczenie zysku dla każdego kwartału
raport['Q1']['zysk'] = raport['Q1']['przychod'] - raport['Q1']['koszt']
raport['Q2']['zysk'] = raport['Q2']['przychod'] - raport['Q2']['koszt']
raport['Q3']['zysk'] = raport['Q3']['przychod'] - raport['Q3']['koszt']
raport['Q4']['zysk'] = raport['Q4']['przychod'] - raport['Q4']['koszt']

# 3. Wyświetlenie tabeli
print("\nKwartał | Przychód | Koszt | Zysk")
print("-" * 38)

print(f"{'Q1':^6} | {raport['Q1']['przychod']:>8} | {raport['Q1']['koszt']:>8} | {raport['Q1']['zysk']:>8}")
print(f"{'Q2':^6} | {raport['Q2']['przychod']:>8} | {raport['Q2']['koszt']:>8} | {raport['Q2']['zysk']:>8}")
print(f"{'Q3':^6} | {raport['Q3']['przychod']:>8} | {raport['Q3']['koszt']:>8} | {raport['Q3']['zysk']:>8}")
print(f"{'Q4':^6} | {raport['Q4']['przychod']:>8} | {raport['Q4']['koszt']:>8} | {raport['Q4']['zysk']:>8}")

# 4. Lista zysków
zyski = [
    raport['Q1']['zysk'],
    raport['Q2']['zysk'],
    raport['Q3']['zysk'],
    raport['Q4']['zysk']
]

# 5. Statystyki zysków
print("\nLista zysków:", zyski)
print("Suma zysków:", sum(zyski))
print("Minimalny zysk:", min(zyski))
print("Maksymalny zysk:", max(zyski))
print("Średni zysk:", sum(zyski) / len(zyski))
