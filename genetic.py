from typing import List, Tuple
from image import Image
from numpy import argsort, random


def create_initial_population() -> List[Image]:
    """
    Create population at step 0
    """

    return [Image(10, 10, []), Image(10, 10, []), Image(10, 10, [])]


def evaluate_population(population: List[Image]) -> List[Image]:
    """
    Calculate fitness per entity, return ordered
    """

    scores = [fitness(entity) for entity in population]
    for i in range(len(population)):
        population[i].fitness = scores[i]

    # sort population in order of scores
    scores, population = zip(*sorted(zip(scores, population), reverse = True))
    # plot best image
    print(f"best image: {scores[0]}")

    return population


def fitness(entity: Image) -> float:
    """
    Calculate score per entity
    """
    return random.random()


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
    return group[0]


def mutate(entity: Image) -> Image:
    """
    Take an image and return (with a certain probability)
    a mutated version
    """
    return entity


def crossover_population(population: List[Image],
                         groupings: List[Tuple[int]]) -> List[Image]:
    """
    Apply crossover between elements in groupings
    """
    old_pop = population

    population = []
    
    # add offspring
    for group in groupings:
        parents = [old_pop[i] for i in group]
        entity = crossover(parents)

        population.append(entity)
    
    # fill to old size with best population entities
    n_add = max(len(old_pop) - len(population), 0)
    population += old_pop[:n_add]

    return population


def mutate_population(population: List[Image]) -> List[Image]:
    return [mutate(entity) for entity in population]


def runga():
    """
    Main loop
    """
    population = create_initial_population(img.shape)

    for gen in range(10):
        print(f"generation {gen}")
        # order population, assign fitnesses
        population = evaluate_population(population)
        groupings  = group_entities(population)
        population = crossover_population(population, groupings)
        population = mutate_population(population)
        print("-"*20)


if __name__ == "__main__":
    runga()



