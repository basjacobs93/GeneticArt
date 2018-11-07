from typing import List
from image import Image
from numpy import argsort


def create_initial_population() -> List[Image]:
	"""
	Create population at step 0
	"""
	pass


def evaluate_population(images: List[Image]) -> List[Image]:
	"""
	Calculate fitness per image, return ordered
	"""

	scores = [fitness(image) for image in images]
	for i in len(images):
		image[i].fitness = scores[i]

	# sort images in order of scores
	scores, images = zip(*sorted(zip(scores, images)))
	print(scores[0])

	return images


def fitness(image: Image) -> float:
	"""
	Calculate score per entity
	"""
	pass


def group_entities(images: List[Image]) -> List[List[Image]]:
	"""
	Take a population and return groups of
	entities to be used in crossover
	"""
	pass


def crossover(group: List[Image]) -> Image:
	"""
	Take a group of parents and return a child
	"""
	pass


def mutate(image: Image) -> Image:
	"""
	Take an image and return (with a certain probability)
	a mutated version
	"""
	pass


def runga():
	"""
	Main loop
	"""
	population = create_initial_population()

	for _ in range(10):
		pass



if __name__ == "__main__":
	runga()



