from typing import Tuple, NewType
from math import sqrt
from loggibud.v1.types import CVRPInstance, Point
from cvrpy.bounds import from_bounds, to_bounds

Pair = NewType('Pair', Tuple[float,float])


def linear_distance(a: Pair, b: Pair) -> float:
    major, minor = (a, b) if a[0] >= b[0] else (b, a)
    return sqrt( (major[0] - minor[0])**2 + (major[1] - minor[1])**2 )


class BoundTransformer:
    '''Pode converter valores de um intervalo [0, 1] para um intervalo de
    quaisquer valores definidos e vice-versa.
    '''
    x_maximum: float
    x_minimum: float
    y_maximum: float
    y_minimum: float

    def __init__(self, xrange: Pair, yrange: Pair):
        self.x_minimum, self.x_maximum = xrange
        self.y_minimum, self.y_maximum = yrange

    @staticmethod
    def from_instance(instance: CVRPInstance):
        '''Pegar os valores máximos e mínimos de latitude e longitude e retorna
        uma instância de BoundTransformer
        '''
        points = [(d.point.lat, d.point.lng) for d in instance.deliveries]
        xmin = min(points, key=lambda p:p[0])[0]
        xmax = max(points, key=lambda p:p[0])[0]
        ymin = min(points, key=lambda p:p[1])[1]
        ymax = max(points, key=lambda p:p[1])[1]
        return BoundTransformer(xrange=(xmin, xmax), yrange=(ymin, ymax))


    def convert_from_point(self, point: Point) -> Pair:
        x = from_bounds(point.lat, self.x_minimum, self.x_maximum)
        y = from_bounds(point.lng, self.y_minimum, self.y_maximum)
        return x, y

    def convert_to_point(self, pair: Pair) -> Point:
        lat = to_bounds(pair[0], self.x_minimum, self.x_maximum)
        lng = to_bounds(pair[1], self.y_minimum, self.y_maximum)
        return Point(lng=lng, lat=lat)
