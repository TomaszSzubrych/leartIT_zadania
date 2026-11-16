pole_imie = "    Alice      "
pole_wiek = "    28       "
pole_email = "    alice@EXAMPLE.com       "

pole_imie_czyste = pole_imie.strip()
pole_wiek_czyste = pole_wiek.strip()
pole_email_czyste = pole_email.strip().lower()

czy_imie_ok = pole_imie_czyste.isalpha()
czy_wiek_ok = pole_wiek_czyste.isdigit()
czy_email_ok = "@" in pole_email_czyste

wszystkie_pola_ok = czy_imie_ok and czy_wiek_ok and czy_email_ok

print(f"Imię po czyszczeniu: {pole_imie_czyste} — poprawne: {czy_imie_ok}")
print(f"Wiek po czyszczeniu: {pole_wiek_czyste} — poprawny: {czy_wiek_ok}")
print(f"E-mail po czyszczeniu: {pole_email_czyste} — poprawny: {czy_email_ok}")
print(f"Wszystkie pola OK? {wszystkie_pola_ok}")
