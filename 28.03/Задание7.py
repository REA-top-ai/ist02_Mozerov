class Circle:

    def __init__(self, diameter):
        print (f"New circle with diameter: {diameter}")
    pi = 3.14

    def area(self, radius):
        return self.pi * radius ** 2

teaching_table = Circle(36)

