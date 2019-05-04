from random import sample
from statistics import mean
from Tree import Individual

K_CONST = 5
MAX_ITERATIONS = 50000
MIN_DELTA = 0.001


class GP:
    def __init__(self, population_size=100, children_size=10, mutation=0.05):
        # dummy population representation
        self.population = [0 for x in range(population_size)]
        self.parents = []
        self.population_size = population_size
        self.children = []
        self.children_size = children_size
        self.mutation = mutation

    def parentSelection(self):
        # K-tournament
        self.parents = []
        for _ in range(self.children_size):
            self.parents += max(sample(self.population, K_CONST))

    def childGeneration(self):
        self.children = [parent_pair[0].recombine(
            parent_pair[1]) for parent_pair in self.parents]

    def recombination(self):
        self.population.append(self.children)
        self.children = []

    def survivalSelection(self):
        # K-tournament
        new_pop = []
        for _ in range(self.population_size):
            new_pop += max(sample(self.population, K_CONST))
        self.population = new_pop

    def evaluate(self):
        for individual in self.population:
            individual.evaluate()

    def not_finished(self, iterations, delta):
        return iterations >= MAX_ITERATIONS or delta <= MIN_DELTA

    def run(self):
        iterations = 0
        delta = 0
        last_avg = 0
        while self.not_finished(iterations, delta):
            iterations += 1
            self.parentSelection()
            self.childGeneration()
            self.recombination()
            self.evaluate()
            avg = mean([i.fitness for i in self.population])
            delta = avg - last_avg
            last_avg = avg
            self.survivalSelection()


# Helper Functions

def pairwise(iterable):
    's -> (s0, s1), (s2, s3), (s4, s5), ...'
    a = iter(iterable)
    return zip(a, a)
