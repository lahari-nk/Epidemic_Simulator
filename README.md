# Epidemic Simulator

This project simulates the spread of an epidemic using a compartmental SEIRV (Susceptible, Exposed, Infectious Asymptomatic, Infectious Symptomatic, Recovered, Vaccinated, Dead) model. The simulation uses real data to estimate parameters and visualizes the epidemic progression over time.

## Features

- **Parameter Estimation:** Automatically estimates transmission, recovery, death, and progression rates from input data.
- **Vaccination & Reinfection:** Models vaccination, natural births/deaths, and possible reinfection after recovery.
- **Hospital Capacity:** Adjusts recovery rate if symptomatic cases exceed hospital capacity.
- **Visualization:** Plots the population in each compartment over time.

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib

Install dependencies with:
```sh
pip install pandas numpy matplotlib
```

## Usage

1. Place your epidemic data CSV file (default: `epidemic_data_30days.csv`) in the same directory.
2. Run the simulator:
   ```sh
   python Epidemic_Simulator.py
   ```
3. The script will print the daily compartment values and display a plot of the simulation.

## Input Data

The CSV file should contain columns:
- `day`, `S`, `E`, `Ia`, `Is`, `R`, `V`, `D`

Each row represents the state of the population on a given day.

## Output

- Daily printout of compartment values.
- A plot showing the evolution of each compartment over time.

## Customization

You can adjust parameters such as:
- `hospital_capacity`
- `vacc_rate`
- `reinfection_days`
- `birth_rate`
- `natural_death_rate`

by editing the variables at the top of the script.

---

**Author:**  
Lahari Naidu Kolli
