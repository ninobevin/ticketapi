import random

class LocationRand:
    # Philippines bounding box (approximate)
    PHILIPPINES_BOUNDS = {
        "min_lat": 4.5,    # Southernmost (Tawi-Tawi)
        "max_lat": 21.0,   # Northernmost (Batanes)
        "min_lon": 116.0,  # Westernmost (Palawan)
        "max_lon": 127.0   # Easternmost (Philippine Sea)
    }

    @staticmethod
    def generate_philippines_location():
        lat = random.uniform(LocationRand.PHILIPPINES_BOUNDS["min_lat"], LocationRand.PHILIPPINES_BOUNDS["max_lat"])
        lon = random.uniform(LocationRand.PHILIPPINES_BOUNDS["min_lon"], LocationRand.PHILIPPINES_BOUNDS["max_lon"])
        return lat, lon