import random
import matplotlib.pyplot as plt

class TemperatureDataGenerator:
    def __init__(self, base=0, delta=0.15, mean=0, std_dev=2.0, uniform_min=-1, uniform_max=1):
        self.base = base
        self.delta = delta
        self.mean = mean
        self.std_dev = std_dev
        self.uniform_min = uniform_min
        self.uniform_max = uniform_max
        self.current = base  # Initial value for the increment/decrement generator

    def __generate_normalized_value(self):
        # Generate a random value between 0 and 1
        return random.random()

    @property
    def random_value(self):
        # Scale the normalized random value to the range [-40, 40]
        x_min = -5
        x_max = 5
        m = x_max - x_min
        c = x_min
        x = self.__generate_normalized_value()
        y = m * x + c
        return y

    def generator_1(self):
        # Generate a constant value
        return 0

    def generator_2(self):
        # Generate a random integer within the uniform distribution range
        return random.randint(self.uniform_min, self.uniform_max)

    def generator_3(self):
        # Generate a random value from a normal distribution
        return random.gauss(self.mean, self.std_dev)

    def generator_4(self, increment=True):
        # Increment or decrement the current value by delta
        if increment:
            self.current += self.delta
        else:
            self.current -= self.delta
        return self.current

    def generate_data(self, num_points=300):
        data = []
        for i in range(num_points):
            # Add peaks and valleys by incrementing/decrementing the base value
            value = self.generator_4((i % 50) > 24)
            # Adjust frequency with normal distribution
            value += self.generator_3()
            # Add squiggles with uniform distribution
            value += self.generator_2() / 20.0
            # Integrate normalized random value scaled to the range [-40, 40]
            value += self.random_value
            # Clamp the value to be within the range [-40, 40]
            value = max(-40, min(40, value))
            data.append(value)
        return data

# # Generate data
# generator = TemperatureDataGenerator()
# data = generator.generate_data()

# # Plotting
# plt.figure(figsize=(18, 6))
# plt.plot(data)
# plt.title('Temperature Data')
# plt.xlabel('Data Point Index')
# plt.ylabel('Temperature (°C)')
# plt.grid(True)
# plt.tight_layout()
# plt.show()
