import math


class Figura:
    def __init__(self, nomi):
        self.nomi = nomi

    def info(self):
        return f"\n--- Shakl: {self.nomi} ---"



class Uchburchak(Figura):
    def __init__(self, a, b, c):
        super().__init__("Uchburchak (Треугольник)")
        self.a = a
        self.b = b
        self.c = c

    def perimetr(self):
        return self.a + self.b + self.c

    def yuza(self):

        s = self.perimetr() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))


class Tortburchak(Figura):
    def __init__(self, a, b):
        super().__init__("To'rtburchak")
        self.a = a
        self.b = b

    def perimetr(self):
        return 2 * (self.a + self.b)

    def yuza(self):
        return self.a * self.b



class Doira(Figura):
    def __init__(self, R):
        super().__init__("Doira")
        self.R = R

    def perimetr(self):

        return 2 * math.pi * self.R

    def yuza(self):
        # Doira yuzasi = pi * R^2
        return math.pi * (self.R ** 2)




uchburchak = Uchburchak(3, 4, 5)
print(uchburchak.info())
print(f"Perimetri: {uchburchak.perimetr()}")
print(f"Yuzasi: {uchburchak.yuza():.2f}")


tortburchak = Tortburchak(5, 10)
print(tortburchak.info())
print(f"Perimetri: {tortburchak.perimetr()}")
print(f"Yuzasi: {tortburchak.yuza()}")


doira = Doira(7)
print(doira.info())
print(f"Perimetri (Uzunligi): {doira.perimetr():.2f}")
print(f"Yuzasi: {doira.yuza():.2f}")