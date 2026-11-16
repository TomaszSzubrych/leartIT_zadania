predykcje = ["spam", "ham", "spam", "spam", "ham", "ham", "spam"]

liczba_spam = predykcje.count("spam")
liczba_ham = predykcje.count("ham")

print(f"spam: {liczba_spam}, ham: {liczba_ham}")
