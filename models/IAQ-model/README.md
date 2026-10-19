# Energy, Comfort, and IAQ Modeling for Window AC Operation

This repository contains a research prototype for evaluating indoor air quality (IAQ) and energy trade-offs under different infiltration and time-of-use (TOU) electricity pricing scenarios.

The main notebook is:

- `Indoor_Air_Quality_model.ipynb`

The notebook combines a Window AC control optimization model with IAQ simulations for CO2 and VOC concentrations. It is intended to support transparent review of the modeling workflow, assumptions, and results.

## Project overview

The purpose of this modeling study is to evaluate how an optimization-based smart thermostat controller can reduce electricity cost and improve thermal comfort for low-income households using window air-conditioning units.

Low-income households often face high energy burdens because of poor building envelopes, high air infiltration, inefficient cooling equipment, and limited flexibility in managing electricity bills. At the same time, Time-of-Use and dynamic electricity pricing programs are becoming more common, but these pricing structures can be difficult for households to interpret and manage manually.

This study formulates a smart control model for window AC operation. The model automatically adjusts cooling decisions based on electricity price, occupancy, and indoor comfort requirements. Its goal is to minimize electricity cost while maintaining acceptable indoor temperature during occupied periods.

The broader purpose is to provide a practical and scalable modeling framework that can help low-income households reduce energy costs, maintain safer indoor temperatures, and participate in demand response programs without requiring technical expertise or major changes in daily routines.

The notebook includes four main components:

1. **Input generation and parameter loading**  
   Model parameters are loaded from a text-based parameter file. Ambient temperature, occupancy-related internal gains, and activity schedules are generated from the specified parameters and random seeds.

2. **Window AC control optimization**  
   A mixed-integer optimization model is implemented in Gurobi. The model determines air-conditioning on/off decisions and associated power use while maintaining indoor temperature constraints.

3. **IAQ simulation**  
   CO2 and VOC concentration profiles are simulated using a mass-balance model with infiltration, outdoor concentration, internal generation, and optional decay/removal.

4. **Scenario comparison and visualization**  
   The notebook evaluates multiple infiltration multipliers and TOU tariff structures, then visualizes the trade-off between energy consumption and IAQ indicators.

The model is used to answer questions such as:

- How much energy and electricity cost are required to maintain acceptable indoor temperature?
- How do CO2 and VOC concentrations change under different infiltration scenarios?
- How do different electricity-pricing structures affect AC operation and energy cost?
- What trade-offs exist between saving energy and maintaining good indoor environmental quality?

The model is a research prototype for scenario comparison and trade-off analysis. Since increasing outdoor-air exchange may help dilute indoor CO2 and VOC concentrations, but it may also increase the cooling load and therefore increase window AC energy consumption. Similarly, reducing AC operation may save energy and cost, but it may lead to higher indoor temperature or poorer indoor air quality. So, the trade-off is evaluated by comparing multiple performance indicators, including: 
- total energy consumption/electricity cost; 
- indoor temperature profile; 
- peak CO2 concentration/duration above the CO2 threshold;
- peak VOC concentration. 

The goal is not to optimize only one metric, but to understand how energy use, cost, thermal comfort, and indoor air quality change together under different scenarios.


## Main dependencies

Run from the repository root or the notebook directory. The notebook loads the external calibration input by a path relative to the current working directory; keep the parameter file alongside the notebook and launch Jupyter from that directory, or pass an explicit path. The parameter file must use one `name = value` entry per line, with values expressed as numeric literals or supported `math`/`numpy` expressions. All referenced model parameters are required. The repository does not contain a calibration file or example calibration values.

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
2. Provide the original calibrated parameter file, `05282025_test.txt`, in the same directory as the notebook, or pass its path to `load_params("path/to/parameters.txt")` in the parameter-loading cell. This file is not tracked in this repository; obtain the authorized project input from its maintainer. Do not substitute guessed calibration values.
3. Open `models/IAQ-model/Indoor_Air_Quality_model.ipynb` in Jupyter Notebook or JupyterLab.
4. Run the notebook cells from top to bottom. The loader checks for the parameter file, parse errors, duplicate keys, and all required parameters, and reports actionable errors.

The optimization cells require a working Gurobi installation and a valid license. Without the parameter file and Gurobi license, the full scenario analysis cannot run.

The notebook will:

1. Load model parameters.
2. Generate synthetic weather, occupancy, and internal gain profiles.
3. Solve the control optimization problem under multiple tariff and infiltration scenarios.
4. Simulate CO2 and VOC concentration profiles.
5. Compute energy and IAQ performance indicators.
6. Generate trade-off plots.

## Model description

The control problem is formulated as a mixed-integer optimization model. The key decision variables include:

- binary air-conditioning operation status
- air-conditioning power
- indoor temperature
- temperature setpoint

The model minimizes energy cost while enforcing indoor temperature dynamics and setpoint-related constraints.

### Optimization Model

Indoor temperature is modeled using a simplified heat-balance equation:

$$T_{t+1}=T_t+\frac{\Delta t}{C}\left[\frac{T^{out}_t - T_t}{R}+Q^{int}_t-\eta P_t\right]$$

where:

$T_t$ is the indoor air temperature at time $t$;\
$T^{out}_t$ is the outdoor temperature at time $t$;\
$C$ is the effective thermal capacitance of the indoor space;\
$R$ is the effective thermal resistance between indoor and outdoor air;\
$Q^{int}_t$ is the internal heat gain from occupants, equipment, or other sources;\
$P_t$ is the window AC power consumption;\
$\eta$ is the cooling effectiveness of the window AC;\
$\Delta t$ is the simulation time step.

This equation represents the indoor heat balance. Indoor temperature changes because of heat transfer from outdoors, internal heat generation, and cooling provided by the window AC. 

Indoor temperature is constrained within an acceptable comfort range: $T^{min} \leq T_t \leq T^{max}$, where $T^{min}$ and $T^{max}$ are the lower and upper indoor temperature limits.

Total Window AC energy consumption is calculated as:

$$E =\sum_{t=0}^{T} P_t \Delta t$$

Electricity cost is calculated as:

$$Cost =\sum_{t=0}^{T} \pi_t P_t \Delta t$$

where:

$E$ is total energy consumption;\
$Cost$ is total electricity cost;\
$\pi_t$ is the electricity price at time $t$.

This formulation allows the model to compare different electricity-pricing structures, such as flat pricing and time-of-use pricing.


### Indoor air quality simulation

Indoor CO₂ concentration is modeled using a mass-balance equation:

$$C^{CO_2}_{t+1}=C^{CO_2}_t+\frac{\Delta t}{V}\left[G^{CO_2}_t+Q^{inf}_t\left(C^{CO_2,out}_t - C^{CO_2}_t\right)\right]$$

where:

$C^{CO_2}_t$ is the indoor CO₂ concentration at time $t$;\
$C^{CO_2,out}_t$ is the outdoor CO₂ concentration;\
$G^{CO_2}_t$ is the indoor CO₂ generation rate;\
$Q^{inf}_t$ is the infiltration or outdoor-air exchange rate;\
$V$ is the indoor air volume.

This equation means that indoor CO₂ increases because of indoor generation and decreases when outdoor-air exchange dilutes indoor air.

Indoor VOC concentration is modeled using a similar mass-balance equation:

$$C^{VOC}_{t+1}=C^{VOC}_t+\frac{\Delta t}{V}\left[G^{VOC}_t+Q^{inf}_t\left(C^{VOC,out}_t - C^{VOC}_t\right)-k^{VOC} V C^{VOC}_t\right]$$

where:

- $C^{VOC}_t$ is the indoor VOC concentration at time $t$;
- $C^{VOC,out}_t$ is the outdoor VOC concentration;
- $G^{VOC}_t$ is the indoor VOC emission rate;
- $Q^{inf}_t$ is the infiltration or outdoor-air exchange rate;
- $k^{VOC}$ is the VOC removal or decay rate;
- $V$ is the indoor air volume.

This equation describes how VOCs accumulate indoors due to emissions and are reduced by ventilation, infiltration, and removal or decay.

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

The current implementation uses a simplified representation of Window AC operation, building thermal dynamics, and IAQ processes. The assumptions are suitable for preliminary scenario analysis but should be refined before operational deployment or policy-level interpretation.


## Citation or acknowledgement

If this repository is used in a proposal, publication, or review process, please cite or acknowledge the associated project documentation and research team as appropriate.
