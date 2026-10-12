
waga = 70
wzrost = 1.75

bmi = waga / (wzrost ** 2)

print(f"BMI: {bmi:.2f}")

if bmi < 18.5:
    print("Interpretacja: Niedowaga")
elif bmi < 25:
    print("Interpretacja: Norma")
else:
    print("Interpretacja: Nadwaga")

