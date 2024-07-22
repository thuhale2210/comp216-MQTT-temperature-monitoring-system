import tkinter as tk
from tkinter import Canvas, Button
from Group_3_Data_Generator import TemperatureDataGenerator
import threading
import time

class TemperatureDynamicChart:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Display")

        # Generate initial data
        self.data_generator = TemperatureDataGenerator()
        self.data = self.data_generator.generate_data(20)
        
        # Create UI
        self.initUI()

    def initUI(self):
        # Start the data updating thread
        self.updating_thread = threading.Thread(target=self.update_data)
        self.updating_thread.daemon = True

        # Create UI elements
        self.label = tk.Label(self.root, text="Temperature Data")
        self.label.grid(row=0, column=1)

        self.label = tk.Label(self.root, text="============================")
        self.label.grid(row=1, column=0)

        self.label = tk.Label(self.root, text="============================")
        self.label.grid(row=1, column=2)

        self.button = Button(self.root, text="Go", command=self.updating_thread.start)
        self.button.grid(row=1, column=1)

        self.canvas = Canvas(self.root, width=600, height=400, bg='pink')
        self.canvas.grid(row=2, column=0, columnspan=3)

    def update_data(self):
        while True:
            # Remove the first item
            self.data.pop(0)
            # Add a new random value to the end of the list
            self.data.append(self.data_generator.random_value)
            # Redraw the chart
            self.draw_chart()
            # Sleep for a short while (0.5 second)
            time.sleep(0.5)

    def draw_chart(self):
        self.canvas.delete('all')
        max_height = 300
        offset_x = 50
        offset_y = -75
        scale = max_height / 80.0
        
        for i in range(1, len(self.data)):
            prev_value = self.data[i - 1] * scale
            curr_value = self.data[i] * scale
            prev_x = offset_x + (i - 1) * 25
            prev_y = offset_y + max_height - prev_value
            curr_x = offset_x + i * 25
            curr_y = offset_y + max_height - curr_value
            
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, fill='red')

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureDynamicChart(root)
    root.mainloop()
