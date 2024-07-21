import tkinter as tk
from tkinter import Canvas, Frame, BOTH, messagebox
from Group_3_Data_Generator import TemperatureDataGenerator

class TemperatureBar(Frame):
    def __init__(self):
        super().__init__()
        self.generator = TemperatureDataGenerator()
        self.value = self.generator.random_value
        self.initUI()

    def initUI(self):
        self.master.title("Temperature Bar")
        self.pack(fill=BOTH)

        self.canvas = Canvas(self, width=400, height=180)
        self.canvas.pack(fill=BOTH)

        self.entry = tk.Entry(self, font=("Arial", 14), width=10, justify='center')
        self.entry.pack(pady=10)

        self.button = tk.Button(self, text="Update Temperature", command=self.update_value, font=("Arial", 12))
        self.button.pack(pady=10)

        self.description = tk.Label(self, text="Lowest: -40\nNormal: -40 to 40\nHighest: 40", font=("Arial", 12))
        self.description.pack(pady=10)

        self.draw_temperature_bar()

    def draw_temperature_bar(self):
        self.canvas.delete("all")

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
        bar_width = (self.value + 40) / 80 * (width - 100)
        self.canvas.create_rectangle(50, 50, 50 + bar_width, height - 50, fill='red')

        # Temp text
        self.canvas.create_text(width // 2, height + 10, text=f"{self.value:.2f}°C", font=("Arial", 14, "bold"))

    def update_value(self):
        try:
            self.value = float(self.entry.get())
            if -40 <= self.value <= 40:
                self.draw_temperature_bar()
            else:
                messagebox.showwarning("Invalid value", "Please enter a value between -40 and 40")
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter a valid number")

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureBar()
    root.geometry("500x370")
    root.mainloop()
