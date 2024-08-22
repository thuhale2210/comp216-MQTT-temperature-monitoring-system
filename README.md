# MQTT Temperature Monitoring System

This project is an MQTT-based temperature monitoring system that consists of a **Publisher** and a **Subscriber**. The Publisher generates temperature data and sends it to a specified MQTT topic, while the Subscriber listens to that topic and displays the data in a visual gauge format.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This system demonstrates a basic implementation of MQTT (Message Queuing Telemetry Transport) for transmitting and visualizing temperature data. The Publisher simulates temperature readings and sends them to a topic on an MQTT broker. The Subscriber receives these readings and displays them using a visual temperature gauge in a Tkinter-based GUI.

## Features

- **Real-time Data Transmission**: Temperature data is transmitted in real-time from the Publisher to the Subscriber.
- **Visual Temperature Gauge**: The Subscriber displays the temperature data using a graphical gauge.
- **Customizable Data Generation**: The Publisher allows for different data generation methods, simulating real-world temperature variations.
- **Cross-platform GUI**: The Subscriber application uses Tkinter, making it compatible with most operating systems.

## Technologies Used

- **Python 3.9**
- **Tkinter**: For creating the GUI of the Subscriber.
- **Paho MQTT**: For handling MQTT communication between the Publisher and Subscriber.
- **Matplotlib**: (Optional) For additional data visualization, if required.

## Setup

### Prerequisites

- **Python 3.9 or above**
- **MQTT Broker**: Install and run [Eclipse Mosquitto](https://mosquitto.org/) or any other MQTT broker.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/thuhale2210/comp216-MQTT-temperature-monitoring-system.git
   cd comp216-MQTT-temperature-monitoring-system
   ```

2. **Install Required Python Packages:**

   ```bash
   pip install paho-mqtt matplotlib
   ```

3. **Start the MQTT Broker:**

   If you're using Mosquitto, start it by running:

   ```bash
   mosquitto
   ```

   Ensure it's running on `localhost:1883` or modify the scripts to match your broker's configuration.

## Running the Project

### Running the Publisher

1. Navigate to the directory containing the Publisher script.
2. Run the Publisher:

   ```bash
   python Group_3_Publisher.py
   ```

   The Publisher will start sending temperature data to the specified MQTT topic.

### Running the Subscriber

1. Navigate to the directory containing the Subscriber script.
2. Run the Subscriber:

   ```bash
   python Group_3_Subscriber_Display_Gauge.py
   python Group_3_Subscriber_Display_Bar.py
   ```

   The Subscriber will connect to the MQTT broker and display the temperature data on a graphical gauge.

## Customization

- **Data Generation**: The `TemperatureDataGenerator` class in the Publisher allows customization of temperature data generation, including random fluctuations, normal distribution, and step increments/decrements.
- **UI Design**: The Tkinter-based gauge can be customized further by modifying the `draw_temperature_gauge` method in the Subscriber.

## Troubleshooting

- **Connection Issues**: Ensure that the MQTT broker is running and accessible from both the Publisher and Subscriber.
- **Data Not Displayed**: Verify that the Publisher and Subscriber are using the same MQTT topic. Also, check the network connectivity if running on different machines.
- **Python Errors**: Ensure all required Python packages are installed and that you are using the correct Python version.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's coding standards and is well-documented.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
