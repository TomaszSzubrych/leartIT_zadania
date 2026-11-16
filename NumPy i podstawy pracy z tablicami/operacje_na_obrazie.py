import numpy as np


# Utworzenie obrazu 100x100
np.random.seed(6)
image = np.random.randint(0, 256, size=(100, 100), dtype=np.uint8)

# Progowanie obrazu z wykorzystaniem boolean indexing
threshold_image = image.copy()
threshold_image[threshold_image < 128] = 0
threshold_image[threshold_image >= 128] = 255

# Utworzenie negatywu obrazu
negative_image = 255 - image

# Dodanie ramki o szerokosci 10 pikseli
padded_image = np.pad(
    image,
    pad_width=10,
    mode="constant",
    constant_values=0
)


# Funkcja prezentujaca ksztalt i wartosci w naroznikach
def show_image_info(title, img):
    print(f"\n{title}")
    print("-" * 45)
    print("Ksztalt:", img.shape)

    print("\nLewy gorny naroznik (5x5):")
    print(img[:5, :5])

    print("\nPrawy gorny naroznik (5x5):")
    print(img[:5, -5:])

    print("\nLewy dolny naroznik (5x5):")
    print(img[-5:, :5])

    print("\nPrawy dolny naroznik (5x5):")
    print(img[-5:, -5:])


# Prezentacja wynikow
print("OPERACJE NA OBRAZIE - NUMPY")
print("=" * 45)

show_image_info("OBRAZ ORYGINALNY", image)
show_image_info("OBRAZ PO PROGOWANIU", threshold_image)
show_image_info("NEGATYW OBRAZU", negative_image)
show_image_info("OBRAZ Z RAMKA 10 PIKSELI", padded_image)
