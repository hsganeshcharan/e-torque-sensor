from flask import Flask, request, jsonify
import numpy as np
import threading
from sklearn.linear_model import LinearRegression
import time
import random
import pandas as pd

app = Flask(__name__)

# Dummy dataset to train the model
# Assume that these are battery features: voltage, temperature, cycles
data = {
    'voltage': [4.2, 4.1, 3.9, 3.8, 4.0],
    'temperature': [25, 30, 28, 35, 32],
    'cycles': [100, 200, 300, 400, 500],
    'health': [100, 85, 70, 50, 30]  # Battery health (%) out of 100
}

# Create a DataFrame
df = pd.DataFrame(data)

# Train a simple linear regression model to predict battery health
X = df[['voltage', 'temperature', 'cycles']]
y = df['health']
model = LinearRegression()
model.fit(X, y)

# Global variable for storing real-time data
battery_data = {
    'voltage': [],
    'temperature': [],
    'cycles': []
}

# Function to simulate collecting real-time data from sensors
def collect_data():
    while True:
        voltage = random.uniform(3.5, 4.2)
        temperature = random.uniform(20, 40)
        cycles = random.randint(100, 1000)

        battery_data['voltage'].append(voltage)
        battery_data['temperature'].append(temperature)
        battery_data['cycles'].append(cycles)

        # Simulate a delay of 2 seconds between data collection
        time.sleep(2)

# API endpoint to predict battery health
@app.route('/predict_battery_health', methods=['GET'])
def predict_battery_health():
    # Get the latest data points
    voltage = battery_data['voltage'][-1] if battery_data['voltage'] else 0
    temperature = battery_data['temperature'][-1] if battery_data['temperature'] else 0
    cycles = battery_data['cycles'][-1] if battery_data['cycles'] else 0

    # Prepare the input for the model
    input_data = np.array([[voltage, temperature, cycles]])

    # Predict the battery health using the trained model
    predicted_health = model.predict(input_data)

    return jsonify({'predicted_battery_health': predicted_health[0]})

# API endpoint to get the latest battery data
@app.route('/battery_data', methods=['GET'])
def get_battery_data():
    # Return the latest data in JSON format
    return jsonify(battery_data)

# Start the data collection in a separate thread
def start_data_collection():
    data_collection_thread = threading.Thread(target=collect_data)
    data_collection_thread.daemon = True
    data_collection_thread.start()

if __name__ == '__main__':
    # Start the data collection thread
    start_data_collection()

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
