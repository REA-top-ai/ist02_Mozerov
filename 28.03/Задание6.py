class Circle:
    pi = 3.14

    def area(self, radius):
        return self.pi * radius ** 2

AreaCalc = Circle()
S = AreaCalc.area(7)
print (S)