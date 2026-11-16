m1 = ["LogisticRegression", 0.78]
m2 = ["RandomForest", 0.92]
m3 = ["SVM", 0.85]
m4 = ["XGBoost", 0.95]

wszystkie = [m1, m2, m3, m4]
accuracy = [m1[1], m2[1], m3[1], m4[1]]

accuracy.sort(reverse=True)
najlepsze_trzy = accuracy[:3]

print(f"Modele i ich wyniki: {wszystkie}")
print(f"Trzy najwyższe wyniki: {najlepsze_trzy}")
print(f"Najwyższe accuracy: {max(accuracy):.2%}")
print(f"Najniższe accuracy: {min(accuracy):.2%}")
