import random
import math
import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, seed, mean, standard_deviation, error_rate=0.0, error_length=0.0, minimum=float('-inf'), maximum=float('inf')):
        random.seed(seed)
        self.mean = mean
        self.standard_deviation = abs(standard_deviation)
        self.step_size_factor = self.standard_deviation / 10
        self.default_error_rate = error_rate
        self.default_error_length = error_length
        self.current_error_rate = error_rate
        self.current_error_length = error_length
        self.minimum = minimum
        self.maximum = maximum
        self.is_current_error = False
        self.value = self.mean - random.random()
        self.last_none_error_value = None
        self.value_count = 0
        self.error_count = 0
        self.factors = [-1, 1]

    def calculate_next_value(self):
        if self.is_current_error:
            self.current_error_length -= 1
            self.current_error_rate = max(self.current_error_length, 0.01)

        next_is_error = random.random() < self.current_error_rate

        if not next_is_error:
            self.next_value()
            if self.is_current_error:
                self.is_current_error = False
                self.current_error_rate = self.default_error_rate
                self.current_error_length = self.default_error_length
        else:
            if not self.is_current_error:
                self.last_none_error_value = self.value
            self.next_error_value()

        return self.value

    def next_value(self):
        self.value_count += 1
        value_change = random.random() * self.step_size_factor
        factor = self.factors[self.decide_factor()]

        if self.is_current_error:
            self.value = self.last_none_error_value + (value_change * factor)
        else:
            self.value += value_change * factor

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

    def next_error_value(self):
        self.error_count += 1

        if not self.is_current_error:
            if self.value < self.mean:
                self.value = random.random() * (self.mean - 3 * self.standard_deviation - self.minimum) + self.minimum
            else:
                self.value = random.random() * (self.maximum - self.mean - 3 * self.standard_deviation) + self.mean + 3 * self.standard_deviation
            self.is_current_error = True
        else:
            value_change = random.random() * self.step_size_factor
            self.value += value_change * self.factors[random.choice([0, 1])]

# Function to calculate the next time interval based on Poisson distribution
def next_time_interval(l):
    n = random.random()
    inter_event_time = -math.log(1.0 - n) / l
    return inter_event_time

# MQTT setup
def mqtt_setup(broker_ip, port=1883, topic="sensor/data"):
    client = mqtt.Client("PC_Publisher")
    client.connect(broker_ip, port)
    return client, topic

def send_data_via_mqtt(client, topic, data):
    client.publish(topic, str(data))
    print(f"Sent data: {data}")

# Main execution with Poisson-distributed intervals
if __name__ == "__main__":
    broker_ip = "192.168.116.139"  
    lambda_rate = 5  # Average rate of 10 messages per second

    # Initialize the simulator and MQTT client
    sim = Simulator(seed=12345, mean=20, standard_deviation=5, error_rate=0.0, error_length=0.0, minimum=0, maximum=40)
    client, topic = mqtt_setup(broker_ip)

    # Generate and send data at Poisson-distributed intervals
    NbreMessages = 100  # Number of messages to publish
    data_values = []  # List to store generated data values for plotting
    timestamps = []   # List to store timestamps for plotting

    start_time = time.time()
    for _ in range(NbreMessages):
        data = sim.calculate_next_value()  # Generate next simulated data value
        data_values.append(data)  # Collect data for plotting
        timestamps.append(time.time() - start_time)  # Collect timestamp relative to start time

        send_data_via_mqtt(client, topic, data)  # Publish the data to MQTT

        # Wait for the next interval based on Poisson process
        time_interval = next_time_interval(lambda_rate)
        time.sleep(time_interval)  # Delay until the next message

    # Disconnect MQTT client
    client.disconnect()

# Plot the data
plt.figure(figsize=(10, 5))
markerline, stemlines, baseline = plt.stem(timestamps, data_values, label="Simulated Sensor Data")
plt.setp(markerline, markersize=5)  # Adjust marker size if needed
plt.xlabel("Time (seconds)")
plt.ylabel("Sensor Value")
plt.title("Sensor Data Over Time with Poisson-distributed Intervals")
plt.legend()
plt.show()

