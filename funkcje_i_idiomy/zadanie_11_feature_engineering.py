
klienci = [
    {"id": 1, "wiek": 25, "dochod": 4500},
    {"id": 2, "wiek": 45, "dochod": 9200},
    {"id": 3, "wiek": 32, "dochod": 6800},
    {"id": 4, "wiek": 28, "dochod": 5200},
    {"id": 5, "wiek": 55, "dochod": 12000}
]


# Funkcja określająca kategorię wiekową
def kategoria_wieku(wiek):
    if wiek < 30:
        return "młody"
    elif wiek <= 50:
        return "średni"
    else:
        return "starszy"


# Funkcja określająca kategorię dochodu
def kategoria_dochodu(dochod):
    if dochod < 5000:
        return "niski"
    elif dochod <= 10000:
        return "średni"
    else:
        return "wysoki"


# List comprehension tworzące nową listę klientów
klienci_z_cechami = [
    {
        **klient,
        "kat_wiekowa": kategoria_wieku(klient["wiek"]),
        "kat_dochodu": kategoria_dochodu(klient["dochod"])
    }
    for klient in klienci
]

for klient in klienci_z_cechami:
    print(klient)

