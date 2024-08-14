import random
from time import asctime
from json import dumps

class Util:
    def __init__(self, start_id=111, base=0, delta=0.15, mean=0, std_dev=5.0, uniform_min=-2, uniform_max=2, wild_chance=0.05):
        # Initialization parameters for flexibility and pattern generation
        self.start_id = start_id
        self.base = base
        self.delta = delta
        self.mean = mean
        self.std_dev = std_dev
        self.uniform_min = uniform_min
        self.uniform_max = uniform_max
        self.current = base
        self.wild_chance = wild_chance  # Probability of generating wild data
    
    def __generate_normalized_value(self):
        return random.random()
    
    @property
    def random_value(self):
        x_min = -5
        x_max = 5
        m = x_max - x_min
        c = x_min
        x = self.__generate_normalized_value()
        y = m * x + c
        return y

    def generator_1(self):
        return 0

    def generator_2(self):
        return random.randint(self.uniform_min, self.uniform_max)

    def generator_3(self):
        return random.gauss(self.mean, self.std_dev)

    def generator_4(self, increment=True):
        if increment:
            self.current += self.delta
        else:
            self.current -= self.delta
        return self.current
    
    def create_data(self, num_points=300):
        # Generates the data value (including logic for regular and wild data)
        if random.random() < self.wild_chance:
            value = random.uniform(-100, 100)  # Wild data range
        else:
            value = self.generator_4((num_points % 50) > 24)
            value += self.generator_3()
            value += self.generator_2() / 20.0
            value += self.random_value
            value = max(-40, min(40, value))  # Normal value range
        
        # Increments the packet ID
        self.start_id += 1
        
        # Creates the JSON object with the necessary fields
        data = {
            'id': self.start_id,
            'time': asctime(),
            'base': self.base,
            'delta': self.delta,
            'mean': self.mean,
            'std_dev': self.std_dev,
            'uniform_min': self.uniform_min,
            'uniform_max': self.uniform_max,
            'normalized_value': self.__generate_normalized_value(),
            'generator_1': self.generator_1(),
            'generator_2': self.generator_2(),
            'generator_3': self.generator_3(),
            'generator_4': self.generator_4(),
            'value': float(value)
        }

        # Returns the data as a JSON object
        return dumps(data, indent=2)
    
    def print_data(self):
        for x in range(5):
            print(self.create_data(x))

# Test the wild data generation
gen = Util()
gen.print_data()
