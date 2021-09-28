from copy import deepcopy
from math import sqrt
from typing import List, Callable, Tuple

import numpy as np
import numpy.random as npr

class Particle:
    '''Classe que representa uma partícula.
    '''
    def __init__(self, objfunction, num_dimensions, range = (0, 1)):
        self.obj_function = objfunction
        self.num_dimensions = num_dimensions
        self.position = npr.uniform(range[0], range[1], size=self.num_dimensions)
        self.fitness_x = None
        self.evaluate()
        # Velocidade inicializada com zeros
        self.velocity = np.zeros(self.num_dimensions)
        # Atual posição é copiada como o Personal Best
        self.personal_best = deepcopy(self.position)
        self.fitness_personal_best = self.fitness_x

    def __str__(self):
        return f"{self.position} => {self.fitness_x:.8}"

    def evaluate(self):
        self.fitness_x = self.obj_function(self.position)

    def copy(self):
        return deepcopy(self)


class Swarm:
    '''Classe que representa um Enxame, possui um conjunto de partículas
    '''
    particles: List[Particle]

    def __init__(self,
        objfunction: Callable,
        num_particles: int,
        num_dimensions: int,
        ptype = Particle
    ):
        self.obj_function = objfunction
        self.num_particles = num_particles
        self.particles = [
            ptype(self.obj_function, num_dimensions) 
            for _ in range(self.num_particles) 
        ]
    
    def __str__(self):
        strings = [ f"{p.fitness_x:.5}" for p in self.particles]
        return "SwarmFit{[" + ", ".join(strings) + "]}"

    def average_fitness(self):
        return (sum([p.fitness_x for p in self.particles]) / self.num_particles)

    def stddev_fitness(self, average=None):
        if average is None:
            average = self.average_fitness()
        return sqrt(
            sum((p.fitness_x - average)**2 for p in self.particles) / float(self.num_particles -1)
        )


class PSO:
    def __init__(self,
        objfunction: Callable,
        num_iterations: int,
        num_particles: int,
        num_dimensions: int,
        range_values = (0., 1.),
        ptype = Particle # Tipo da partícula
    ):
        self.objective_function = objfunction
        self.num_iterations = num_iterations
        self.num_particles = num_particles
        self.num_dimensions = num_dimensions
        self.range_values = range_values
        # Definição de contantes e parâmetros do PSO
        self.c1 = 2.05
        self.c2 = 2.05
        self.w_range = (.4, .9)
        self.w = np.array([
            self.w_range[1] - (
                self.w_range[1] - self.w_range[0]) * i / self.num_iterations
            for i in range(self.num_iterations) 
        ])
        self.max_velocity = (self.range_values[1] - self.range_values[0]) / 2.0
        # Instanciação do enxame
        self.swarm = Swarm(objfunction, self.num_particles, num_dimensions, ptype=ptype)
        self.convergence = np.array([], dtype=float)


    def move_particle(self, particle: Particle):
        '''Movimenta uma partícula no espaço de busca
        '''
        assert len(particle.position) == len(particle.velocity)
        particle.position = particle.position + particle.velocity

        for i in range(particle.num_dimensions):
            if particle.position[i] < self.range_values[0]:
                particle.position[i] = self.range_values[0]
            if particle.position[i] > self.range_values[1]:
                particle.position[i] = self.range_values[1]
        return


    def update_velocity(self, i: int, particle: Particle, g_best: Particle):
        '''Atualização da velocidade de uma partícula
        '''
        r1 = npr.random(particle.num_dimensions)
        r2 = npr.random(particle.num_dimensions)

        particle.velocity = (
            self.w[i] * particle.velocity +
            self.c1 * r1 * (particle.personal_best - particle.position) +
            self.c2 * r2 * (g_best.position - particle.position)
        )

        for j in range(len(particle.velocity)):
            if abs(particle.velocity[j]) > self.max_velocity:
                particle.velocity[j] = np.sign(particle.velocity[j]) * self.max_velocity
        
    
    def get_global_best(self) -> Particle:
        '''Retorna o atual Global Best do enxame
        '''
        fitness_list = [ p.fitness_x for p in self.swarm.particles ]
        minor_index = fitness_list.index(min(fitness_list))
        return self.swarm.particles[minor_index].copy()

    
    # Atualiza o Personal Best de uma partícula e, se for o caso,
    # o Global Best do enxame
    def update_bests(self, p: Particle, g_best: Particle):
        if p.fitness_x <= p.fitness_personal_best:
            p.personal_best = deepcopy(p.position)
            p.fitness_personal_best = p.fitness_x
            if p.fitness_x <= g_best.fitness_x:
                g_best.position = deepcopy(p.position)
                g_best.fitness_x = p.fitness_x
            

    # Fazer a avaliação de uma partícula
    @staticmethod
    def evaluate(particle: Particle):
        particle.evaluate()


    def optimize(self):
        '''Inicia o processo de busca usando o algoritmo de PSO
        '''
        g_best = self.get_global_best()
        self.convergence = np.array([], dtype=float)

        for t in np.arange(self.num_iterations):
            for i in np.arange(self.num_particles):
                self.update_velocity(t, self.swarm.particles[i], g_best)
                self.move_particle(self.swarm.particles[i])
                self.evaluate(self.swarm.particles[i])
                self.update_bests(self.swarm.particles[i], g_best)

            self.convergence = np.append(self.convergence, g_best.fitness_x)

        return g_best
        
