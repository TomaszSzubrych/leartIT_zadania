e1 = ["Exp_01", 0.85, 1.23]
e2 = ["Exp_02", 0.89, 4.56]
e3 = ["Exp_03", 0.87, 7.89]

separator = "=" * 44

print(separator)
print(f"{'Experiment':<16}{'Accuracy':>14}{'Time (s)':>14}")
print(separator)
print(f"{e1[0]:<16}{e1[1]:>13.2%}{e1[2]:>14.2f}")
print(f"{e2[0]:<16}{e2[1]:>13.2%}{e2[2]:>14.2f}")
print(f"{e3[0]:<16}{e3[1]:>13.2%}{e3[2]:>14.2f}")
print(separator)
