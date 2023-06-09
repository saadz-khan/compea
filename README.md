# CoMPEA
Cognitive Power Metering and Predictions using Edge AI - Final Year Project (FYP) - Bachelors of Electrical Engineering

### Overview
This project proposes an intelligent home solar system that uses machine learning techniques to predict future power generation and consumption in households. The system aims to optimize energy usage and reduce reliance on traditional power sources, leading to cost savings and decreased environmental impact. The system incorporates various sensors and meters to collect data on solar energy generation and weather conditions. This data is then fed into a machine learning algorithm to predict future power generation patterns depending on the weather conditions. The project implements a web-based interface that allows users to monitor their energy usage and control the system remotely. Results from the implementation of the system show an accuracy rate of over 90% in predicting power generation and consumption, leading to an improvement in overall energy efficiency.

<iframe src="https://docs.google.com/gview?url=https://github.com/saadz-khan/compea/blob/master/assets/poster.pdf&embedded=true" width="100%" height="600px"></iframe>

The project is divided into two main components: Hardware and Software.

### File Structure
```
final-year-project
├── README.md
├── LICENSE
├── .gitignore
├── hardware
│   ├── README.md
│   ├── weather-node
│   │   ├── weather_node.ino
│   │   └── README.md
│   ├── generation-node
│   │   ├── generation_node.ino
│   │   └── README.md
│   └── master-node
│       ├── master_node.ino
│       └── README.md
└── software
    ├── README.md
    ├── auto-forecasting
    │   └── (all files related to the auto-forecasting pipeline)
    ├── consumption-pipeline
    │   └── (all files related to the consumption pipeline)
    ├── solar-power-dashboard
    │   └── (all files related to the dashboard)
    └── quantum-machine-learning
        └── (all files related to the quantum machine learning work)
```

### Hardware
The hardware component of this project involves the use of Arduino and ESP based hardware to collect data on solar energy generation and weather conditions. This data is then processed and transmitted to a Firebase real-time database for further analysis. The hardware component is divided into three nodes: the Weather Node, the Generation Node, and the Master Node.

- Weather Node: Responsible for measuring solar irradiation, temperature, and humidity. It uses a BH-1750 digital light sensor to measure solar irradiation, a DHT-22 sensor to measure temperature and humidity, an Arduino UNO microcontroller board to process the sensor data, and an NRF-24L01 wireless transceiver module to send the collected data to the Master Node.

- Generation Node: Connected to the on-grid inverter and monitors the power generation data. It uses an ACS-712 current sensor to measure the current output of solar panels, a ZMPT101B voltage sensor to measure the voltage output of solar panels, an Arduino Nano microcontroller board to process the sensor data, and an NRF-24L01 wireless transceiver module to send the collected data to the Master Node.

- Master Node: Receives the data transmitted from both the Weather Node and the Generation Node. It uses an ESP8266 Wi-Fi microcontroller to process and structure the received data, and an NRF-24L01 wireless transceiver module to receive data from the secondary nodes. The processed data is then uploaded to a Firebase real-time database.

### Software
The software component of this project involves the use of machine learning techniques to predict future power generation and consumption patterns. It is divided into four main parts:

#### Auto-forecasting
The Auto-forecasting pipeline predicts the daily yield of a solar power plant. It fetches the data from Firebase, preprocesses it, trains an LSTM model, evaluates its performance, and uploads the predicted data back to Firebase. The pipeline is set up to run automatically every Monday at midnight and can be triggered manually using GitHub Actions. For more details, refer to the README.md file in the auto-forecasting directory.

#### Consumption Pipeline
The Consumption pipeline forecasts electrical power consumption using a Long Short-Term Memory (LSTM) neural network and an AutoRegressive Integrated Moving Average (ARIMA) model. The pipeline is designed to download and preprocess the data, train and evaluate the models, and upload the results to Firebase. For more details, refer to the README.md file in the consumption-pipeline directory.

#### Solar Power Dashboard
The Solar Power Dashboard is a web-based interface that allows users to monitor their energy usage and control the system remotely. It is built with React.js and has a backend on Firebase. The dashboard displays real-time data on power generation and consumption, as well as predictions for future energy usage. For more details, refer to the README.md file in the solar_power-dashboard directory.

#### Quantum Machine Learning
The Quantum Machine Learning work is a future work for the LSTM based forecasting. It is currently under development and aims to enhance the accuracy and efficiency of the forecasting models using quantum computing techniques. For more details, refer to the README.md file in the quantum-machine-learning directory.
