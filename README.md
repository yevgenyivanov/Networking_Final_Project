# Python Script README

This README file provides an overview of a Python script designed to analyze network packet data and generate various types of graphs. The script utilizes the Scapy library for network packet processing, pandas for data manipulation, numpy for numerical computations, and matplotlib for graph generation. The script reads data from CSV files containing network packet information and generates PDF function graphs, Inter-Message-Delay (IMD) graphs, and Complementary Cumulative Distribution Function (CCDF) graphs.

## Prerequisites

Before using the Python script, ensure you have the following prerequisites:

1. Python 3.x installed.
2. Required libraries: scapy, pandas, numpy, and matplotlib. You can install them using the following command:

```bash
pip install scapy pandas numpy matplotlib
```
3. Placed .csv files inside the ```resources/csvs/``` directory
## How to use
To use the Python script, follow these steps:

1. Download or clone the repository to your local machine.
2. Open a terminal and navigate to the downloaded folder.
3. Run the following command to execute the script:
```bash
python ./src/main.py
```
4. To see the generated graphs, check the ```results/``` folder

## Graph Generation
The script generates the following types of graphs from interpreted CSV files:

- PDF Function Graph
The PDF (Probability Density Function) function graph displays the probability density of inter-message delays within network packet data.

- Inter-Message-Delay (IMD) Graph
The IMD graph represents packet length over time intervals, providing insights into network traffic patterns.

- Complementary Cumulative Distribution Function (CCDF) Graph
The CCDF graph illustrates the complementary cumulative distribution of normalized message sizes, helping analyze message size distribution.

## Notes
 - Please ensure that all columns required by the script's methods are present and correctly named in the CSV files used for analysis. The script depends on specific column names for accurate graph generation.
 - The script deletes *all* files and directories that may be present in the ```results/``` folder. If you need to make any backups, move the files to a different, *external* directory.

## Explained Examples
TODO

