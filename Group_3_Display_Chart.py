import tkinter as tk
from tkinter import Canvas, Entry, Button, messagebox
from Group_3_Data_Generator import TemperatureDataGenerator

class TemperatureDisplayChart:
    def __init__(self, root):
        self.root = root
        self.root.title("Historical Data")

        # Generate initial data
        self.data_generator = TemperatureDataGenerator()
        self.data = self.data_generator.generate_data(20)
        
        # Create UI
        self.initUI()

    def initUI(self):
        # Create UI elements
        self.label_info = tk.Label(self.root, text="Data range:")
        self.label_info.grid(row=0, column=0)

        self.entry = Entry(self.root)
        self.entry.grid(row=0, column=1)

        self.button = Button(self.root, text="Go", command=self.draw_charts)
        self.button.grid(row=0, column=2)

        self.label_range = tk.Label(self.root, text="")
        self.label_range.grid(row=1, column=0, columnspan=3)
        
        self.canvas = Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=3)

    def draw_charts(self):
        self.canvas.delete('all')
        try:
            start_index = 0
            if self.entry.get() != "":
                start_index = int(self.entry.get())
            if start_index < 0 or start_index + 5 >= len(self.data):
                raise ValueError("Index out of range")
            self.label_range.config(text=f"Data range: {start_index} - {start_index + 5}")
            self.draw_rectangles_and_lines(start_index)
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter a valid integer within the range 0 - 20")

    def draw_rectangles_and_lines(self, start_index):
        bar_width = 40
        max_height = 300
        spacing = 10
        offset_x = 125
        offset_y = -75
        scale = max_height / 80.0
        
        for i in range(6):
            value = self.data[start_index + i]
            bar_height = value * scale
            x0 = offset_x + (bar_width + spacing) * i
            y0 = offset_y + max_height - bar_height
            x1 = x0 + bar_width
            y1 = offset_y + max_height
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='#cbc0d3')
            if i > 0:
                prev_value = self.data[start_index + i - 1]
                prev_height = prev_value * scale
                prev_x = offset_x + (bar_width + spacing) * (i - 1) + bar_width / 2
                prev_y = offset_y + max_height - prev_height
                curr_x = x0 + bar_width / 2
                curr_y = y0
                
                self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, fill='#564a69')

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureDisplayChart(root)
    root.mainloop()
