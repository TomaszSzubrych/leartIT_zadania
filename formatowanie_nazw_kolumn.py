
nazwa_raw = " PATIENT_age_YEARS "

nazwa = nazwa_raw.strip()
nazwa = nazwa.lower()
nazwa = nazwa.replace("_", " ")
nazwa = nazwa.title()

print(nazwa)
