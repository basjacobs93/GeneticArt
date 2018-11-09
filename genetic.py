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


def evaluate_population(population: List[Image]) -> List[Image]:
    """
    Calculate fitness per entity, return ordered
    """

    scores = [fitness(entity) for entity in population]
    for i in range(len(population)):
        population[i].fitness = scores[i]

    # sort population in order of scores
    scores, population = zip(*sorted(zip(scores, population), reverse = True))

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
    return [(i, len(population)-i-1) for i in range(0, len(population)//2)]


def crossover(group: List[Image]) -> Image:
    """
    Take a group of parents and return a child
    """
    elems = [elem.copy() for entity in group for elem in entity.elements]

    # Child has average number of elements
    avg_len = len(elems) // len(group)

    inds = np.random.choice(len(elems), size = avg_len, replace = False)
    return Image((IM_SIZE, IM_SIZE), [elems[ind] for ind in inds])


def mutate(entity: Image) -> Image:
    """
    Take an image and return (with a certain probability)
    a mutated version
    """

    new_entity = entity.copy()

    # 80% change of not doing anything
    if np.random.random() > 0.2:
        return new_entity

    rnd = np.random.random()

    # change order of elements
    if rnd < 0.25:
        np.random.shuffle(new_entity.elements)

    # resize a random element
    elif rnd < 0.5:
        elem_id = np.random.randint(0, len(new_entity.elements))
        new_entity.elements[elem_id].mutate()

    # remove element
    elif rnd < 0.75:
        del_id = np.random.randint(len(new_entity.elements))
        del new_entity.elements[del_id]

    # add element
    else:
        # max 10 elements
        if len(new_entity.elements) < 10:
            xmin, xmax, ymin, ymax = np.random.randint(0, IM_SIZE, size = 4)
            color = np.random.random(3)
            rect = Rectangle(xmin, xmax, ymin, ymax, color)
            new_entity.elements.append(rect)
    
    new_entity.generate()

    return new_entity


def crossover_population(population: List[Image],
                         groupings: List[Tuple[int]]) -> List[Image]:
    """
    Apply crossover between elements in groupings
    """

    # keep best couple of elements
    offspring = []
    
    # add offspring
    for group in groupings:
        parents = [population[i] for i in group]
        entity = crossover(parents)

        offspring.append(entity)

    return offspring


def mutate_population(population: List[Image]) -> List[Image]:
    return [mutate(entity) for entity in population]


def runga():
    """
    Main loop
    """
    population = create_initial_population()

    last_fitness = 0

    for gen in range(N_GEN):
        # order population, assign fitnesses
        population = evaluate_population(population)

        # plot best image
        if population[0].fitness > last_fitness:
            last_fitness = population[0].fitness
            print(f"{last_fitness}")
            # plt.show()
            # plt.pause(0.0001)
            population[0].save(f"progress/{gen}.jpg")


        # best individuals survive
        n = POP_SIZE//3
        survivors  = population[:n + (POP_SIZE % 3)]
        groupings  = group_entities(population[:(2*n)])
        children   = crossover_population(population[:(2*n)], groupings)
        mutants    = mutate_population(population[:n])
        population = survivors + children + mutants

    population[0].save("out.jpg")


if __name__ == "__main__":
    POP_SIZE = 200
    N_GEN = 1000
    IM_SIZE = 100

    url = "daysofwineandroses.jpg"
    img = imread(url)
    img = resize(img, (IM_SIZE, IM_SIZE), mode='reflect', anti_aliasing=True)
    plt.imshow(img)
    plt.ion()
    # plt.show()
    # plt.pause(0.0001)

    runga()



