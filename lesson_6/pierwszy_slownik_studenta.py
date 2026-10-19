
# Utworzenie słownika
student = {
    'imie': 'Kamil',
    'nazwisko': 'Nowak',
    'wiek': 22,
    'kierunek': 'Informatyka'
}

# Dodanie adresu e-mail
student['email'] = 'kamil.nowak@edu.pl'

# Zmiana wieku
student['wiek'] = 23

# Wyświetlenie informacji za pomocą f-stringa
print(
    f"Student: {student['imie']} {student['nazwisko']} "
    f"({student['wiek']} lata), kierunek: {student['kierunek']}, "
    f"email: {student['email']}"
)

# Wyświetlenie kluczy i wartości
print("Klucze:", list(student.keys()))
print("Wartości:", list(student.values()))
