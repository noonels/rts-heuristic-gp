class GP:
	def __init__(self, population=100, children=10, mutation=0.05):
		self.population = [0 for x in range(population)] #dummy population representation
		self.children = children
		self.mutation = mutation

	def parentSelection(self):
		#TODO: k-tournament, FPS, uniform random
		pass

	def childGeneration(self):
		pass #this functionality could be included in parent selection

	def survivalSelection(self):
		#TODO: k-tournament without replacement, FPS, uniform random
		pass

	def run(self):
		#TODO: number of evaluations, survival strategies, termination conditions
		#while !terminate:
			#parents = parentSelection()
			#population.append(childGeneration(parents))
			#survivalSelection()
		pass