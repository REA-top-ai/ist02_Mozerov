class Circle:
    pi = 3.14

    def __init__(self, diameter):
        self.radius = diameter/2
        print (f"New circle with diameter: {diameter}")

    def circumference(self):
        return 2 * self.pi * self.radius

    def area(self, radius):
        return self.pi * radius ** 2

medium_pizza = Circle(12)
teaching_table = Circle(36)
round_room = Circle(11460)

print (medium_pizza.circumference(), teaching_table.circumference(), round_room.circumference(), sep="\n")