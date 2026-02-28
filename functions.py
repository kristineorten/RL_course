import numpy as np
from cell import Cell

def find_location_in_array(location: Cell, locations: list[Cell]):
    locations = np.array(locations)
    index = np.where(locations == location)[0]
    if (index.size == 0):
        return None
    else:
        return index[0]