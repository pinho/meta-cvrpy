def to_bounds(value: float, low: float, high: float) -> float:
    assert low < high
    assert 0. <= value <= 1.
    return high - (high - low)*value

def from_bounds(value: float, low: float, high: float) -> float:
    assert low < high
    assert low <= value <= high
    return (low - value)/(low - high)