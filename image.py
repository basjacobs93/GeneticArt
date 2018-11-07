from typing import List
from pandas import DataFrame
from plotnine import *

class Shape(List):
	def __init__(self, info: dict) -> None:
		self.df = DataFrame(info)

	def __print__(self) -> None:
		print(self.df.values)

class Rectangle(Shape):
	def show(self) -> geom_rect:
		return geom_rect(
			data = self.df,
			mapping = aes(xmin = "xmin", xmax = "xmax",
						  ymin = "ymin", ymax = "ymax"),
			fill = self.df.color)


class Image(List):
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

    def __print__(self) -> None:
    	for element in elements:
    		print(element)
    		print("-"*10)


if __name__ == "__main__":
	rect1 = Rectangle({"xmin": [2], "xmax": [3], "ymin": [2], "ymax": [3], "color": ["blue"]})
	rect2 = Rectangle({"xmin": [4], "xmax": [7], "ymin": [5], "ymax": [6], "color": ["red"]})
	print(rect1)
	im = Image(10, 10, [rect1, rect2])
	im.show()