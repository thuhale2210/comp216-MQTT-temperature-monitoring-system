import random
import paho.mqtt.client as mqtt
from time import sleep
from Group_3_util import Util
import tkinter as tk
from tkinter import ttk

class PublisherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Publisher")

        # GUI elements for delay and topic
        ttk.Label(root, text="Delay (s):").grid(column=0, row=0, padx=10, pady=10)
        self.delay_var = tk.DoubleVar(value=0.75)
        ttk.Entry(root, textvariable=self.delay_var).grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(root, text="Topic:").grid(column=0, row=1, padx=10, pady=10)
        self.topic_var = tk.StringVar(value="Temperature")
        ttk.Entry(root, textvariable=self.topic_var).grid(column=1, row=1, padx=10, pady=10)

        # Button to start publishing
        ttk.Button(root, text="Start Publishing", command=self.start_publishing).grid(column=0, row=2, columnspan=2, padx=10, pady=10)

        self.gen = Util()
        self.client = mqtt.Client()
        self.skip_block_chance = 0.1  # Probability to skip a block of transmissions

    def start_publishing(self):
        delay = self.delay_var.get()
        topic = self.topic_var.get()
        self.publish(delay, topic, times=10)

    def publish(self, delay, topic, times=1):
        for x in range(times):
            print(f'#{x}', end=' ')
            if random.random() > 0.01:  # Non-deterministic skipping: Miss transmission 1 in 100 times
                if random.random() > self.skip_block_chance:
                    self.__publish(topic, delay)
                else:
                    print("Block of transmissions skipped!")  # Skip block of transmissions
                    sleep(delay * 5)  # Simulate a pause for the skipped block
            else:
                print("Transmission skipped!")  # Indicate a single missed transmission

    def __publish(self, topic, delay):
        data = self.gen.create_data() # Generates the data, which includes timestamp and packet ID
        print(f'{data} to broker')
        self.client.connect('localhost', 1883)
        self.client.publish(topic, payload=data) # Sending data (Publishes the JSON object to the broker)
        sleep(delay)  # Necessary to prevent the client from disconnecting too
        self.client.disconnect()

if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherApp(root)
    root.mainloop()
