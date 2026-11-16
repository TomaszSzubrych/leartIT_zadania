# Wyniki modeli przed uporządkowaniem
wyniki = [0.78, 0.92, 0.85, 0.88, 0.81, 0.95, 0.79]

wyniki.sort(reverse=True)
najlepsze_trzy = wyniki[:3]

print(f"Wyniki od najlepszego: {wyniki}")
print("Trzy najlepsze wyniki:")
print(f"1. {najlepsze_trzy[0]:.2%}")
print(f"2. {najlepsze_trzy[1]:.2%}")
print(f"3. {najlepsze_trzy[2]:.2%}")
