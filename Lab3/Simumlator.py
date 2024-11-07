import random
import matplotlib.pyplot as plt

class SensorSimulator:
    def __init__(self, seed, mean, standard_deviation):
        random.seed(seed)
        self.mean = mean
        self.standard_deviation = abs(standard_deviation)
        self.step_size_factor = self.standard_deviation / 10
        self.value = self.mean - random.random()
        self.factors = [-1, 1]

    def calculate_next_value(self):
        value_change = random.random() * self.step_size_factor
        factor = self.factors[self.decide_factor()]
        self.value += value_change * factor
        return self.value

    def decide_factor(self):
        if self.value > self.mean:
            distance = self.value - self.mean
            continue_direction = 1
            change_direction = 0
        else:
            distance = self.mean - self.value
            continue_direction = 0
            change_direction = 1

        chance = (self.standard_deviation / 2) - (distance / 50)
        random_value = random.random() * self.standard_deviation

        return continue_direction if random_value < chance else change_direction

# Initialize simulator with given parameters
simulator = SensorSimulator(seed=12345, mean=20, standard_deviation=5)

# Generate 1000 values for plotting
data_set = [simulator.calculate_next_value() for _ in range(2000)]

# Plot the generated sensor data
plt.figure(figsize=(10, 6))
plt.plot(data_set, label="Simulated Sensor Data")
plt.xlabel("Time Steps")
plt.ylabel("Sensor Value")
plt.title("Simulated Sensor Data over Time")
plt.legend()
plt.grid(True)
plt.show()
