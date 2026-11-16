# Pomiary temperatury z kolejnych siedmiu dni
temperatury = [22.5, 23.0, 21.5, 24.0, 23.5, 22.0, 23.0]

pierwszy_dzien = temperatury[0]
ostatni_dzien = temperatury[-1]
srodek_tygodnia = temperatury[2:5]

print(f"Temperatura pierwszego dnia: {pierwszy_dzien:.1f} °C")
print(f"Temperatura ostatniego dnia: {ostatni_dzien:.1f} °C")
print(f"Temperatury z trzech środkowych dni: {srodek_tygodnia}")
