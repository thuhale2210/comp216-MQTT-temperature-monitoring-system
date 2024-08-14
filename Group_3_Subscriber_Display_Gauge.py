import math
import paho.mqtt.client as mqtt
import json
import tkinter as tk
from tkinter import Canvas, Frame, BOTH, Label, messagebox

class TemperatureGaugeSubscriber(Frame):
    def __init__(self, root, topic='TEMPERATURE'):
        super().__init__()
        self.root = root
        self.value = 0  # Initialize value

        # Setup MQTT client to receive data
        self.client = mqtt.Client()
        self.client.on_message = self.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)        
        self.client.loop_start()

        # Initialize UI
        self.master.title("Temperature Gauge")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1, pady=20)
        self.label = Label(root, text=f'Subscriber listening to : {topic}\n...', font=("Helvetica", 12))
        self.label.pack(fill=BOTH)

    def draw_temperature_gauge(self):
        self.canvas.delete("all")

        width = 400
        height = 300
        radius = 150
        center_x = width // 2
        center_y = height // 2 + 50

        # Background circle
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                outline='black', fill='Light grey', width=4)

        # Markings
        for i in range(-40, 45, 5):
            angle = 180 - (i + 40) / 80 * 180
            x1 = center_x + (radius - 20) * math.cos(math.radians(angle))
            y1 = center_y - (radius - 20) * math.sin(math.radians(angle))
            x2 = center_x + radius * math.cos(math.radians(angle))
            y2 = center_y - radius * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            x_text = center_x + (radius - 35) * math.cos(math.radians(angle))
            y_text = center_y - (radius - 35) * math.sin(math.radians(angle))
            self.canvas.create_text(x_text, y_text, text=str(i), font=("Arial", 10))

        # Labels
        self.canvas.create_text(center_x, center_y - radius - 20, text="Temperature (°C)", font=("Arial", 14, "bold"))

        # Gauge hand based on the value
        angle = 180 - (self.value + 40) / 80 * 180
        hand_length = radius - 30
        hand_x = center_x + hand_length * math.cos(math.radians(angle))
        hand_y = center_y - hand_length * math.sin(math.radians(angle))
        self.canvas.create_line(center_x, center_y, hand_x, hand_y, fill='red', width=4)

        # Center point
        self.canvas.create_oval(center_x - 10, center_y - 10, center_x + 10, center_y + 10, outline='black', fill='black')

        # Temp text
        self.canvas.create_text(center_x, center_y + radius + 30, text=f"{self.value:.2f}°C", font=("Arial", 14, "bold"))

    # Decode the message and handle the data
    def message_handler(self, client, userdata, message):
        data = message.payload.decode("utf-8")
        obj = json.loads(data)
        value = obj["value"]
        print(f'\n{message.topic} \n{value}(val)')
        
        # Detecting and handling out of range (erroneous) data (wild data)
        if value < -40 or value > 40:
            messagebox.showwarning("Wild Data Detected!", f"Value {value} is out of range!")
            self.label.config(text=f"Wild Data: {value} detected at {obj['time']}")
        else:
            # Handle sensible data and display in text and visual format
            self.value = value
            self.draw_temperature_gauge()
            self.label.config(text=f"Received value: {value} at {obj['time']}")

    def block(self):
        self.root.mainloop()

# Run the Subscriber with Temperature Gauge UI
root = tk.Tk()
root.title("MQTT Subscriber - Temperature Gauge")
root.geometry("400x500")
sub = TemperatureGaugeSubscriber(root)
sub.block()
