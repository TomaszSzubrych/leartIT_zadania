linia = "Alice,28,Data Scientist,75000"
pola = linia.split(",")

imie = pola[0]
wiek = int(pola[1])
zawod = pola[2]
pensja = int(pola[3])

print(f"{imie} ma {wiek} lat, pracuje jako {zawod} i zarabia ${pensja}")
