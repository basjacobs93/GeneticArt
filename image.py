from typing import List
from pandas import DataFrame
from plotnine import *


class Shape(List):
    """
    Generic type of a shape
    """
    def __init__(self, **kwargs) -> None:
        self.df = DataFrame({k: [v] for k, v in kwargs.items()})


class Rectangle(Shape):
    """
    Rectangle, should have xmin, xmax, ymin and ymax
    """
    def show(self) -> geom_rect:
        return geom_rect(
            data = self.df,
            mapping = aes(xmin = "xmin", xmax = "xmax",
                          ymin = "ymin", ymax = "ymax"),
            fill = self.df.color)


class Image(List):
    """
    Image built from Shapes
    """
    def __init__(self, width: float, height: float,
                 elements: List[Shape]) -> None:
        self.elements = elements
        self.width = width
        self.height = height
        self.fitness = None
        pass

    def show(self) -> None:
        plot = (ggplot() +
                # make plot white, add border
                theme(line = element_blank(),
                      text = element_blank(),
                      title = element_blank(),
                      plot_background = element_blank(),
                      panel_border = element_rect(colour = "black",
                                                    fill = None, size = 1)) +
                xlim(0, self.width) + ylim(0, self.height))
        # add elements to plot
        for element in self.elements:
            plot += element.show()
        print(plot)


if __name__ == "__main__":
    rect1 = Rectangle(xmin = 2, xmax = 3, ymin = 2, ymax = 3, color = "blue")
    rect2 = Rectangle(xmin = 4, xmax = 7, ymin = 5, ymax = 6, color = "red")
    im = Image(10, 10, [rect1, rect2])
    im.show()
