import pandas as pd
import numpy as np

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(df)}")

# Usuwamy obserwacje bez wieku, ponieważ nie można ich przypisać
# do przedziału wiekowego.

df_age = df[["Age", "Survived"]].dropna().copy()

print(f"Liczba pasażerów z podanym wiekiem: {len(df_age)}")

# ============================================================
# 2. FUNKCJA OBLICZAJĄCA SURVIVAL RATE W PRZEDZIAŁACH
# ============================================================

def calculate_survival_rate(data, bin_column):
    result = (
        data.groupby(bin_column, observed=True)["Survived"]
        .agg(["mean", "count"])
        .reset_index()
    )

    result["Survival_Rate_%"] = result["mean"] * 100

    return result.drop(columns=["mean"])


def calculate_spread(result):
    rates = result["Survival_Rate_%"]

    return rates.max() - rates.min()


# ============================================================
# 3. STRATEGIA 1 — EQUAL-WIDTH BINNING
# ============================================================

df_age["Equal_Width"] = pd.cut(
    df_age["Age"],
    bins=5
)

equal_width_result = calculate_survival_rate(
    df_age,
    "Equal_Width"
)

equal_width_spread = calculate_spread(
    equal_width_result
)

print("\n=== STRATEGIA 1: EQUAL-WIDTH ===")
print(
    equal_width_result.round(2).to_string(index=False)
)

print(f"Rozpiętość survival rate: {equal_width_spread:.2f} pp")

# ============================================================
# 4. STRATEGIA 2 — EQUAL-FREQUENCY BINNING
# ============================================================

df_age["Equal_Frequency"] = pd.qcut(
    df_age["Age"],
    q=5
)

equal_frequency_result = calculate_survival_rate(
    df_age,
    "Equal_Frequency"
)

equal_frequency_spread = calculate_spread(
    equal_frequency_result
)

print("\n=== STRATEGIA 2: EQUAL-FREQUENCY ===")
print(
    equal_frequency_result.round(2).to_string(index=False)
)

print(f"Rozpiętość survival rate: {equal_frequency_spread:.2f} pp")

# ============================================================
# 5. STRATEGIA 3 — RĘCZNA OPTYMALIZACJA
# ============================================================

manual_bins = [
    [0, 12, 18, 35, 60, 100],
    [0, 8, 15, 25, 40, 60, 100],
    [0, 6, 14, 22, 30, 45, 65, 100]
]

manual_results = []

for number, bins in enumerate(manual_bins, start=1):

    column_name = f"Manual_{number}"

    df_age[column_name] = pd.cut(
        df_age["Age"],
        bins=bins,
        include_lowest=True
    )

    result = calculate_survival_rate(
        df_age,
        column_name
    )

    spread = calculate_spread(result)

    manual_results.append({
        "Strategia": number,
        "Granice": bins,
        "Wyniki": result,
        "Rozpiętość": spread
    })

    print(f"\n=== RĘCZNE BINNING — ZESTAW {number} ===")
    print(f"Granice: {bins}")
    print(result.round(2).to_string(index=False))
    print(f"Rozpiętość survival rate: {spread:.2f} pp")

# ============================================================
# 6. WYBÓR NAJLEPSZEGO ZESTAWU RĘCZNEGO
# ============================================================

best_manual = max(
    manual_results,
    key=lambda item: item["Rozpiętość"]
)

print("\n=== NAJLEPSZY ZESTAW RĘCZNY ===")
print(f"Zestaw: {best_manual['Strategia']}")
print(f"Granice: {best_manual['Granice']}")
print(f"Rozpiętość: {best_manual['Rozpiętość']:.2f} pp")

# ============================================================
# 7. PORÓWNANIE TRZECH STRATEGII
# ============================================================

comparison = pd.DataFrame({
    "Strategia": [
        "Equal-width",
        "Equal-frequency",
        f"Manual — zestaw {best_manual['Strategia']}"
    ],
    "Liczba przedziałów": [
        len(equal_width_result),
        len(equal_frequency_result),
        len(best_manual["Wyniki"])
    ],
    "Rozpiętość Survival Rate (pp)": [
        equal_width_spread,
        equal_frequency_spread,
        best_manual["Rozpiętość"]
    ]
})

comparison = comparison.sort_values(
    "Rozpiętość Survival Rate (pp)",
    ascending=False
)

print("\n=== PORÓWNANIE STRATEGII BINNINGU ===")
print(comparison.round(2).to_string(index=False))

# ============================================================
# 8. REKOMENDACJA
# ============================================================

best_strategy = comparison.iloc[0]

print("\n=== REKOMENDACJA ===")
print(
    f"Największą separację klas uzyskała strategia: "
    f"{best_strategy['Strategia']}."
)

print(
    f"Rozpiętość survival rate wynosi "
    f"{best_strategy['Rozpiętość Survival Rate (pp)']:.2f} "
    f"punktów procentowych."
)

print(
    "Rekomendacja opiera się na kryterium maksymalnej "
    "różnicy między najwyższym i najniższym survival rate."
)

# ============================================================
# 9. WERYFIKACJA KOŃCOWA
# ============================================================

print("\n=== WERYFIKACJA KOŃCOWA ===")

print(f"Liczba pasażerów z wiekiem: {len(df_age)}")
print(f"Strategie porównane: {len(comparison)}")
print(f"Zestawy ręczne przetestowane: {len(manual_results)}")

