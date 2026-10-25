
slowa = ["python", "data", "science", "machine", "learning", "AI"]

dlugosci = [len(slowo) for slowo in slowa]

slownik_dlugosci = {
    slowo: len(slowo) for slowo in slowa
}

print(f"Lista długości: {dlugosci}")
print(f"Słownik długości: {slownik_dlugosci}")
