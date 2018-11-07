from typing import List, Tuple
from skimage.io import imread, imshow, show
from skimage.transform import resize
import numpy as np

from matplotlib import pyplot as plt

from image import Image, Rectangle


def random_image() -> Image:
    n_rects = np.random.randint(1, 5)
    rects = []

    for _ in range(n_rects):
        xmin, xmax, ymin, ymax = np.random.randint(0, IM_SIZE, size = 4)
        color = np.random.random(3)
        rect = Rectangle(xmin, xmax, ymin, ymax, color)
        rects.append(rect)

    return Image((IM_SIZE, IM_SIZE), rects)


def create_initial_population() -> List[Image]:
    """
    Create population at step 0
    """

    return [random_image() for _ in range(POP_SIZE)]


def evaluate_population(population: List[Image], show: bool) -> List[Image]:
    """
    Calculate fitness per entity, return ordered
    """

    scores = [fitness(entity) for entity in population]
    for i in range(len(population)):
        population[i].fitness = scores[i]

    # sort population in order of scores
    scores, population = zip(*sorted(zip(scores, population), reverse = True))
    # plot best image
    if show:
        print(f"fitness: {np.round(scores[:3], 2)}, {np.round(scores[-3:], 2)}")
        population[0].show()

    return list(population)


def fitness(entity: Image) -> float:
    """
    Calculate score per entity
    """
    return entity.diff(img)


def group_entities(population: List[Image]) -> List[Tuple[int]]:
    """
    Take a population and return groups of
    entities to be used in crossover
    """
    return [(i, i+1) for i in range(0, len(population)//2, 2)]


def crossover(group: List[Image]) -> Image:
    """
    Take a group of parents and return a child
    """

    elems = [elem for entity in group for elem in entity.elements]

    inds = np.random.choice(len(elems), size = len(group[0].elements), replace = False)
    return Image((IM_SIZE, IM_SIZE), [elems[ind] for ind in inds])


def mutate(entity: Image) -> Image:
    """
    Take an image and return (with a certain probability)
    a mutated version
    """

    # change order of elements
    if np.random.random() < 0.2:
        np.random.shuffle(entity.elements)

    # resize a random element
    if np.random.random() < 0.2:
        elem_id = np.random.randint(0, len(entity.elements))
        entity.elements[elem_id].mutate()
        # make sure entity knows its elements have changed
        entity.generate()

    return entity


def crossover_population(population: List[Image],
                         groupings: List[Tuple[int]]) -> List[Image]:
    """
    Apply crossover between elements in groupings
    """
    old_pop = population

    # keep best third of elements
    population = old_pop[:POP_SIZE//3]
    
    # add offspring
    for group in groupings:
        parents = [old_pop[i] for i in group]
        entity = crossover(parents)

        population.append(entity)
    
    # fill to old size with worst population entities
    if POP_SIZE > len(population):
        population += old_pop[len(population):]

    return population


def mutate_population(population: List[Image]) -> List[Image]:
    # mutate the worst entities
    mutants = [mutate(entity) for entity in population]
    mutant_ids = np.random.choice(range(len(mutants)), size = POP_SIZE-POP_SIZE//4, replace = False)

    return population[:POP_SIZE//4] + mutants[mutant_ids]

def runga():
    """
    Main loop
    """
    population = create_initial_population()

    for gen in range(N_GEN):
        # order population, assign fitnesses
        population = evaluate_population(population, (gen % 10) == 9)
        groupings  = group_entities(population)
        population = crossover_population(population, groupings)
        population = mutate_population(population)


if __name__ == "__main__":
    POP_SIZE = 100
    N_GEN = 1000
    IM_SIZE = 100

    url = "blueslidepark.jpg"
    img = imread(url)
    img = resize(img, (IM_SIZE, IM_SIZE), mode='reflect', anti_aliasing=True)
    plt.imshow(img)
    plt.ion()
    plt.show()
    plt.pause(0.001)

    runga()



