'''Implementação do algoritmo de Random Walk
'''

from numpy.random import random
from loggibud.v1.types import CVRPInstance

from cvrpy.particle.decoder import ParticleDecoder
from cvrpy.route_functions import total_distance

class Individual:
    values: list
    fitness: float

    def __init__(self, instance: CVRPInstance, num_vehicles: int):
        self.problem = instance
        self.size = len(self.problem.deliveries) + 2*num_vehicles
        self.values = random(self.size)
        self.fitness = None
        
    def __str__(self):
        return f'{self.values} => {self.fitness}'
    
    def evaluate(self):
        solution = ParticleDecoder.decode(self.values, self.problem)
        self.fitness = total_distance(solution)
        

class RandomWalk:
    def __init__(self, num_individuals):
        self.num_individuals = num_individuals
        self.population = list()
        self.convergence = list()
        
    def display_population(self, iteration=None):
        if iteration: print(f'Iteração {iteration}:')
        for indi in self.population:
            print(indi)
        print()
        
    def get_convergence(self):
        return self.convergence
        
    def run(self, until, problem: CVRPInstance, num_vehicles: int, verbose=False):
        self.convergence.clear()
        num_iterations = until
        self.population = [
            Individual(problem, num_vehicles)
            for _ in range(self.num_individuals)
        ]
        
        for indi in self.population:
            indi.evaluate()
            
        if verbose: self.display_population()
        
        for i in range(num_iterations):
            self.population.sort(key=lambda x: x.fitness)
            middle_index = int(len(self.population)/2)
            self.population = self.population[:middle_index]
            
            while (len(self.population) < self.num_individuals):
                new_indi = Individual(problem, num_vehicles)
                new_indi.evaluate()
                self.population.append(new_indi)
                
            fitnesses = [ indi.fitness for indi in self.population ]
            self.convergence.append(min(fitnesses))
                
            if verbose: self.display_population(i+1)
        
        return self.population[0]