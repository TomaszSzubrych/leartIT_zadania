raw_col = " Customer ID "

clean_col = raw_col.strip().lower().replace(" ", "_")

print(f"Nazwa przed czyszczeniem: '{raw_col}'")
print(f"Nazwa po czyszczeniu:     '{clean_col}'")
