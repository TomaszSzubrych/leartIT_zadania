
lr_initial = 0.1
decay = 0.95
epoch = 10

lr_new = lr_initial * (decay ** epoch)

print(f"Learning rate po 10 epokach: {lr_new:.2e}")
