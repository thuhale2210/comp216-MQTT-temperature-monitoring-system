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

        # Create an event to control the thread execution
        self.pause_event = threading.Event()
        self.pause_event.set()  # Start in a running state

        # Create UI
        self.initUI()

    def initUI(self):
        # Create UI elements
        self.label = tk.Label(self.root, text="Temperature Data", font='Helvetica 18 bold italic')
        self.label.grid(row=0, column=1, columnspan=3)

        self.label = tk.Label(self.root, text="==========================")
        self.label.grid(row=1, column=0)

        self.label = tk.Label(self.root, text="==========================")
        self.label.grid(row=1, column=4)

        self.go_button = Button(self.root, text="Go", width="8", command=self.start_thread)
        self.go_button.grid(row=1, column=1)

        self.pause_button = Button(self.root, text="Pause", width="8", command=self.pause_thread)
        self.pause_button.grid(row=1, column=2)

        self.exit_button = Button(self.root, text="Exit", width="8", command=root.quit)
        self.exit_button.grid(row=1, column=3)

        self.canvas = Canvas(self.root, width=800, height=400, bg='pink')
        self.canvas.grid(row=2, column=0, columnspan=5)

    def start_thread(self):
        # Start the data updating thread
        self.updating_thread = threading.Thread(target=self.update_data)
        self.updating_thread.daemon = True
        self.updating_thread.start()

    def pause_thread(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pause_button.config(text="Resume")
        else:
            self.pause_event.set()
            self.pause_button.config(text="Pause")

    def update_data(self):
        while True:
            self.pause_event.wait()  # Wait until the event is set (resumed)
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
        offset_x = 125
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