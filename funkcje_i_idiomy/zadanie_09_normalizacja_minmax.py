
def normalize_minmax(dane):
    if not dane:
        return []

    minimum = min(dane)
    maksimum = max(dane)

    if maksimum == minimum:
        return [0 for _ in dane]

    wynik = [
        (x - minimum) / (maksimum - minimum)
        for x in dane
    ]

    return wynik


wynagrodzenie = [3500, 4200, 5800, 7200, 9500, 4800, 6100]

wynagrodzenie_znormalizowane = normalize_minmax(wynagrodzenie)

print(f"Wynagrodzenia: {wynagrodzenie}")
print(f"Wynagrodzenia znormalizowane: {wynagrodzenie_znormalizowane}")
