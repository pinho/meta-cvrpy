from typing import Callable
from numpy import ndarray
from numpy.random import random
from loggibud.v1.types import CVRPInstance

from cvrpy.pso import Particle

class ParticleFactory:
    @staticmethod
    def create_for(instance: CVRPInstance, objective: Callable, num_vehicles: int) -> Particle:
        num_customers = len(instance.deliveries)
        size = num_customers + 2*num_vehicles
        particle = Particle(objective, size)
        return particle
