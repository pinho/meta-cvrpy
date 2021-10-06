import json
import requests
from numpy import ndarray
from loggibud.v1.types import CVRPSolution, CVRPSolutionVehicle, Point

from cvrpy.particle.decoder import ParticleDecoder

BASE_URL = "http://localhost:5000"

def request_distance_between(a: Point, b: Point) -> float:
    '''Faz a requisição para o serviço de rotas do OSRM passando dois pontos
    como parâmetros e retorna somente o valor de distância percorrida entre eles
    '''
    url = f'{BASE_URL}/route/v1/drive/{a.lng},{a.lat};{b.lng},{b.lat}'

    response = requests.get(url, params={
            'alternatives': 'false',
            'steps': 'false',
            'overview': 'false'
        })

    if 200 <= response.status_code < 300:
        data = json.loads(response.content)
        return data['routes'][0]['distance']
    else:
        print(f'Erro na requisição GET {response.url}')
        return 0.


def vehicle_distance_traveled(vehicle: CVRPSolutionVehicle) -> float:
    '''Calcula a distância percorrida por um mesmo veículo partindo da origem e
    passando por todos os pontos de entrega, e por último voltando para a origem
    '''
    distance = 0.

    if len(vehicle.deliveries) > 0:
        distance += request_distance_between(vehicle.origin, vehicle.deliveries[0].point)
        for i, delivery in enumerate(vehicle.deliveries):
            next_i = i+1
            if next_i < len(vehicle.deliveries):
                next_delivery = vehicle.deliveries[next_i]
                distance += request_distance_between(delivery.point, next_delivery.point)
            pass

        distance += request_distance_between(vehicle.deliveries[-1].point, vehicle.origin)

    return distance


def total_distance(solution: CVRPSolution) -> float:
    '''Função objetivo

    Função a ser otimizada, retorna a soma de todas as distâncias entre pares de
    pontos calculadas através das distâncias percorridas por cada veículo.
    Recebe um array, que deve ser a posição de um partícula.
    '''
    sums = [vehicle_distance_traveled(v) for v in solution.vehicles]
    return sum(sums)