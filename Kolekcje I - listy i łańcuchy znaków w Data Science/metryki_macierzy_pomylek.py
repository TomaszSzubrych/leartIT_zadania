# Macierz pomyłek: TN, FP, FN, TP
cm = [
    [80, 10],
    [5, 45]
]

tn = cm[0][0]
fp = cm[0][1]
fn = cm[1][0]
tp = cm[1][1]

accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)

print(f"TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")
print(f"Accuracy:  {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
