# 3GPP TS 32.432 XML to ELK Stack Integration

## Overview

This project demonstrates how to generate and import 3GPP TS 32.432 XML files into the ELK Stack (Elasticsearch, Logstash, Kibana) for real-time analysis and visualization for an imaginary scenario. 

The project covers the entire process, from generating XML files with simulated data to configuring Logstash to parse and index the data into Elasticsearch, and finally, creating a Kibana dashboard for visualization.

## Features

- **XML File Generation**: A Python script is provided to generate realistic 3GPP TS 32.432 XML files containing performance measurement data.
- **Logstash Configuration**: Custom Logstash configuration for parsing the XML files, handling namespaces, and using XPath to extract and split fields.
- **Kibana Visualization**: An example Kibana dashboard to visualize hardware utilization metrics extracted from the XML files.

## Prerequisites

- **Python 3.x**: Required to run the XML generation script.
- **ELK Stack**: Ensure you have Elasticsearch, Logstash, and Kibana installed. The examples were tested on Windows instance

## Project Structure

```
├── README.md                     # This README file
├── export.ndjson                 # Example Kibana dashboard and visualizations
├── generate_test_xmls.py         # Python script to generate 3GPP TS 32.432 XML files
├── hardware_utilization.csv      #
├── results/                      # Directory where generated XML files are stored
├── test.conf                     # Logstash configuration file for testing
└── threegpp.conf                 # Logstash configuration file 
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to contact me.


