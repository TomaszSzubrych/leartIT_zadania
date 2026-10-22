
wyniki = [78, 92, 65, 88, 95, 71, 85]

maksimum = wyniki[0]

for wynik in wyniki:
    if wynik > maksimum:
        maksimum = wynik

print(f"Największa wartość: {maksimum}")
