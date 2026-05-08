# Indoor Air Quality (IAQ) Model
# IAQ–Energy Trade-off Optimization and Simulation

This repository contains a research prototype for evaluating indoor air quality (IAQ) and energy trade-offs under different infiltration and time-of-use (TOU) electricity pricing scenarios.

The main notebook is:

- `Wellcome_Trust_0505.ipynb`

The notebook combines an HVAC control optimization model with IAQ simulations for CO2 and VOC concentrations. It is intended to support transparent review of the modeling workflow, assumptions, and results.

## Project overview

The workflow studies how building ventilation/infiltration levels and electricity tariff structures affect:

- HVAC energy consumption
- electricity cost
- indoor temperature control
- peak CO2 concentration
- VOC peak concentration and exposure
- IAQ–energy trade-offs across multiple scenarios

The notebook includes four main components:

1. **Input generation and parameter loading**  
   Model parameters are loaded from a text-based parameter file. Ambient temperature, occupancy-related internal gains, and activity schedules are generated from the specified parameters and random seeds.

2. **HVAC control optimization**  
   A mixed-integer optimization model is implemented in Gurobi. The model determines air-conditioning on/off decisions and associated power use while maintaining indoor temperature constraints.

3. **IAQ simulation**  
   CO2 and VOC concentration profiles are simulated using a mass-balance model with infiltration, outdoor concentration, internal generation, and optional decay/removal.

4. **Scenario comparison and visualization**  
   The notebook evaluates multiple infiltration multipliers and TOU tariff structures, then visualizes the trade-off between energy consumption and IAQ indicators.


## Main dependencies

The notebook uses the following Python packages:

- `gurobipy`
- `numpy`
- `pandas`
- `matplotlib`

It also uses standard Python libraries including:

- `ast`
- `math`
- `re`
- `pathlib`

A Gurobi installation and a valid Gurobi license are required to run the optimization model.

## Suggested installation

Create and activate a Python environment, then install the required packages:

```bash
pip install numpy pandas matplotlib gurobipy
```

Gurobi also needs to be installed and licensed separately. Please refer to the official Gurobi installation instructions for your operating system and license type.

## How to run

1. Clone or download the repository.
2. Place inputfile in the same folder as `Wellcome_Trust_0505.ipynb`.
3. Open the notebook in Jupyter Notebook.
4. Run the notebook cells from top to bottom.

The notebook will:

1. Load model parameters.
2. Generate synthetic weather, occupancy, and internal gain profiles.
3. Solve the HVAC control optimization problem under multiple tariff and infiltration scenarios.
4. Simulate CO2 and VOC concentration profiles.
5. Compute energy and IAQ performance indicators.
6. Generate trade-off plots.

## Model description

### HVAC optimization

The HVAC control problem is formulated as a mixed-integer optimization model. The key decision variables include:

- binary air-conditioning operation status
- air-conditioning power
- indoor temperature
- temperature setpoint

The model minimizes energy cost while enforcing indoor temperature dynamics and setpoint-related constraints.

### Indoor air quality simulation

IAQ is simulated using a concentration mass-balance model

## Scenario design

The notebook currently evaluates:

- Multiple infiltration multipliers
- Multiple electricity tariff structures:
  - flat tariff
  - two-period TOU tariff
  - aggressive TOU tariff

For each scenario, the workflow computes:

- total energy consumption
- electricity cost
- CO2 peak concentration
- hours above a CO₂ threshold
- VOC peak concentration
- VOC exposure

## Outputs

The main outputs include:

- A scenario-level results table, stored in the notebook as `df_tradeoff`
- Scatter plots showing:
  - energy consumption vs. CO2 peak concentration
  - energy consumption vs. VOC exposure

These outputs are intended to help compare how different ventilation/infiltration assumptions and electricity tariffs influence both energy performance and IAQ outcomes.

## Notes

This repository is a research prototype. The current notebook is intended to demonstrate the modeling and computational workflow rather than provide a finalized software package.


## Limitations

The current implementation uses a simplified representation of HVAC operation, building thermal dynamics, and IAQ processes. The assumptions are suitable for preliminary scenario analysis but should be refined before operational deployment or policy-level interpretation.


## Citation or acknowledgement

If this repository is used in a proposal, publication, or review process, please cite or acknowledge the associated project documentation and research team as appropriate.

## Original Source

Adapted from work contributed by Ziwei Liu:
https://github.com/zliu72-utk/Wellcome-Trust

