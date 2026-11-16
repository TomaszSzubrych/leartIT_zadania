wpis_logu = "2024-01-15 10:23:45 ERROR Training failed due to OOM"
fragmenty = wpis_logu.split(" ", 3)

data = fragmenty[0]
czas = fragmenty[1]
poziom = fragmenty[2]
wiadomosc = fragmenty[3]

dopuszczalne_poziomy = ["INFO", "WARNING", "ERROR", "DEBUG"]
poziom_znany = poziom in dopuszczalne_poziomy

print(f"[{data} {czas}] {poziom}: {wiadomosc}")
print(f"Czy poziom logu jest rozpoznawany? {poziom_znany}")
