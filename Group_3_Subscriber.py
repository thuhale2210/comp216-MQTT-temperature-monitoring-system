import paho.mqtt.client as mqtt
import json
from tkinter import messagebox, Tk, Label

class SubscriberApp:
    def __init__(self, root, topic='Temperature'):
        self.root = root
        # Listen to messages from the broker under an agreed topic
        self.client = mqtt.Client()
        self.client.on_message = self.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)        
        self.client.loop_start()

        self.label = Label(root, text=f'Subscriber listening to : {topic}\n...', font=("Helvetica", 12))
        self.label.pack(pady=20)
    
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
            # Handle sensible data and display in text format
            self.label.config(text=f"Received value: {value} at {obj['time']}")
        
    def block(self):
        self.root.mainloop()

# Run the Subscriber
root = Tk()
root.title("Subscriber")
root.geometry("400x200")
sub = SubscriberApp(root)
sub.block()
