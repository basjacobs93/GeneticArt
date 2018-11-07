from typing import List, Tuple
from pandas import DataFrame
from skimage import draw
from skimage import io
import numpy as np
from matplotlib import pyplot as plt

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
        return draw.rectangle(start = (self.xmin, self.ymin),
                         end   = (self.xmax, self.ymax),
                         shape = shape)

    def mutate(self):
        xmin = self.xmin + np.random.randint(11) - 5
        xmax = self.xmax + np.random.randint(11) - 5
        ymin = self.ymin + np.random.randint(11) - 5
        ymax = self.ymax + np.random.randint(11) - 5
        color = np.clip(self.color + np.random.random(3) - 0.5, 0, 1)
        return Rectangle(xmin, xmax, ymin, ymax, color)

    def __str__(self):
        return f"from: ({self.xmin}, {self.ymin}), to: ({self.xmax}, {self.ymax})"


class Image(List):
    """
    Image built from Shapes
    """
    def __init__(self, shape: Tuple[int],
                 elements: List[Shape]) -> None:
        self.elements = elements
        self.shape = shape
        self.fitness = None

        self.generate()

    def generate(self) -> np.ndarray:
        """
        Create matrix image representation
        """
        img = np.ones((self.shape[0], self.shape[1], 3), dtype=float)

        for element in self.elements:
            rr, cc = element.generate(self.shape)
            img[rr, cc] = element.color

        self.img = img

    def show(self) -> None:
        plt.imshow(self.img)
        plt.ion()
        plt.show()
        plt.pause(0.001)


    def diff(self, img: np.ndarray) -> float:
        """
        Calculate difference between images
        """
        return 1 - np.mean(np.sum(abs(img-self.img), axis = 2)/3)

