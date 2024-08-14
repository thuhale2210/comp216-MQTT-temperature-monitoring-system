import paho.mqtt.client as mqtt
import json
import tkinter as tk
from tkinter import messagebox, Tk, Label, Canvas, BOTH, Frame

class TemperatureBarSubscriber(Frame):
    def __init__(self, root, topic='TEMPERATURE'):
        super().__init__()
        self.root = root

        # Listen to messages from the broker under an agreed topic
        self.client = mqtt.Client()
        self.client.on_message = self.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)        
        self.client.loop_start()
        
        # Creates UI elements to display the data values
        self.master.title("Temperature Bar")
        self.pack(fill=BOTH)
        self.canvas = Canvas(root, width=400, height=200)
        self.canvas.pack(fill=BOTH, expand=1, pady=20)
        self.label = Label(root, text=f'Subscriber listening to : {topic}\n...', font=("Helvetica", 12))
        self.label.pack(fill=BOTH)
    
    def draw_temperature_bar(self, value):
        self.canvas.delete("all")
        
        # size of the bar
        width = 500
        height = 150

        # Title
        self.canvas.create_text(width // 2, 20, text="Temperature (°C)", font=("Arial", 14, "bold"))

        # Background bar
        self.canvas.create_rectangle(50, 50, width - 50, height - 50, fill='light grey')

        # Markings
        for i in range(-40, 45, 5):
            x = 50 + (i + 40) / 80 * (width - 100)
            self.canvas.create_line(x, height - 50, x, height - 40, fill="black", width=2)
            self.canvas.create_text(x, height - 20, text=str(i), font=("Arial", 10))

        # Temperature bar based on the value
        bar_width = (value + 40) / 80 * (width - 100)
        self.canvas.create_rectangle(50, 50, 50 + bar_width, height - 50, fill='red')

        # Temp text
        self.canvas.create_text(width // 2, height + 10, text=f"{value:.2f}°C", font=("Arial", 14, "bold"))
            
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
            self.draw_temperature_bar(value)
            self.label.config(text=f"Received value: {value} at {obj['time']}")
        
    def block(self):
        self.root.mainloop()

# Run the Subscriber
root = Tk()
root.title("MQTT Subscriber - Temperature Bar")
root.geometry("500x300")
sub = TemperatureBarSubscriber(root)
sub.block()
