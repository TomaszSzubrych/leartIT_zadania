
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c):
    return c + 273.15


temperatury = [0, 10, 20, 30, 37, 100]

print(f"{'°C':>8} {'°F':>10} {'K':>10}")

for c in temperatury:
    f = celsius_to_fahrenheit(c)
    k = celsius_to_kelvin(c)

    print(f"{c:8.1f} {f:10.2f} {k:10.2f}")
