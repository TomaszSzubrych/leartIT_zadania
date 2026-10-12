
accuracy_a = 0.87
czas_a = 120

accuracy_b = 0.89
czas_b = 450

roznica = accuracy_b - accuracy_a

print(f"Accuracy modelu A: {accuracy_a:.2%}")
print(f"Accuracy modelu B: {accuracy_b:.2%}")
print(f"Różnica accuracy: {roznica:.2%}")

if roznica > 0.02:
    print("Różnica accuracy jest znacząca.")
else:
    print("Różnica accuracy nie jest większa niż 2 punkty procentowe.")

print(f"Czas treningu modelu A: {czas_a} s")
print(f"Czas treningu modelu B: {czas_b} s")

if accuracy_b > accuracy_a and czas_b > czas_a:
    print("Model B jest dokładniejszy, ale trenuje się dłużej.")

if accuracy_a >= accuracy_b - 0.02 and czas_a < czas_b:
    print("Rekomendacja: Model A to najlepszy kompromis.")
else:
    print("Rekomendacja: Model B zapewnia lepszą dokładność.")
