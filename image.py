from typing import List, Tuple
from pandas import DataFrame
#from plotnine import *
from skimage.draw import rectangle
from skimage import io
import numpy as np
import skimage

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

    def __init__(self, xmin: float, xmax: float,
                 ymin: float, ymax: float, color: Tuple[int]) -> None:
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.color = color

    def generate(self, shape: Tuple) -> List[int]:
        return rectangle(start = (self.xmin, self.ymin),
                         end   = (self.xmax, self.ymax),
                         shape = shape)


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

        self.img = self.generate()

    def generate(self) -> np.ndarray:
        """
        Create matrix image representation
        """
        img = np.ones((self.width, self.height, 3), dtype=float)

        for element in self.elements:
            rr, cc = element.generate((self.width, self.height))
            img[rr, cc] = element.color

        return img

    def show(self) -> None:
        io.imshow(self.img)
        io.show()


if __name__ == "__main__":
    #skimage.io.use_plugin("pil")
    rect1 = Rectangle(xmin = 2, xmax = 3, ymin = 2, ymax = 3, color = (0.1, 0.4, 0.1))
    rect2 = Rectangle(xmin = 4, xmax = 7, ymin = 5, ymax = 6, color = (0.4, 0.1, 0.1))
    rect3 = Rectangle(xmin = 1, xmax = 6, ymin = 8, ymax = 9, color = (0.4, 0.2, 0.8))
    im = Image(10, 10, [rect1, rect2, rect3])
    im.show()


