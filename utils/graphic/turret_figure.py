import utils as lines


def to_data(self,line_graphics,x,y):
    for graphic in line_graphics:
        if graphic["type"] == "circle":
            circle = lines.Circle(graphic, x, y)
            self.armocircles.append(lines.Circle.to_dict(circle))
        elif graphic["type"] == "trapezoid":
            trapezoid = lines.Trapezoid(graphic, x, y)
            self.armotrapezoids.append(lines.Trapezoid.to_dict(trapezoid))
        elif graphic["type"] == "triangle":
            triangle = lines.Triangle(graphic, x, y)
            self.armotriangles.append(lines.Triangle.to_dict(triangle))