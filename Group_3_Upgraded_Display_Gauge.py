import tkinter as tk
from tkinter import Canvas, Frame, BOTH
import math
import paho.mqtt.client as mqtt
import json

class TemperatureGauge(Frame):
    def __init__(self, root, topic='Temperature'):
        super().__init__(root)
        self.value = 0  # Initialize value
        self.initUI()

        # Setup MQTT client to receive data
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        self.client.loop_start()

    def initUI(self):
        self.master.title("Temperature Gauge")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1, pady=20)

        self.description = tk.Label(self, text="Lowest: -40\nNormal: -40 to 40\nHighest: 40", font=("Arial", 12))
        self.description.pack(pady=10)

        self.draw_temperature_gauge()

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

    def on_message(self, client, userdata, message):
        data = message.payload.decode("utf-8")
        obj = json.loads(data)
        self.value = obj.get("value", 0)  # Use get to avoid KeyError
        self.draw_temperature_gauge()

if __name__ == "__main__":
    root = tk.Tk()
    topic_name = "Temperature"
    app = TemperatureGauge(root, topic=topic_name)
    root.geometry("400x500")
    root.mainloop()
