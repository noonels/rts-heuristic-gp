class GP:
    def __init__(self, population=100, children=10, mutation=0.05):
        self.population = [0 for x in range(population)] #dummy population representation
        self.children = children
        self.mutation = mutation

    def parentSelection(self):
        # K-tournament
        # self.population = [max([self.population[randInt(self.population.length)] for i in range(k)]) for n in range(l)]
        pass

    def childGeneration(self, parents):
        pass

    def survivalSelection(self, k=10, l=100):
        # self.population = [max([self.population[randInt(self.population.length)] for i in range(k)]) for n in range(l)]
        pass

    def run(self):
    # TODO: number of evaluations, survival strategies, termination conditions
    # while !terminate:
    #   parents = parentSelection()
    #   population.append(childGeneration(parents))
    #   survivalSelection()
        pass
