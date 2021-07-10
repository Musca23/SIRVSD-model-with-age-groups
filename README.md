# SIRVSD model with age groups
Implementation of a SIRVSD model with different age groups and heterogeneous contacs in Python for Computational Models for Complex Systems Course.<br>
Check the [presentation](https://github.com/Musca23/SIRVSD-model-with-age-groups/blob/main/SIRVSD_model_presentation_MURGIA_PDF.pdf) to get an idea of ​​how the model was defined and for the results of the qualitative analysis (also present in the [Jupyter Notebook](https://github.com/Musca23/SIRVSD-model-with-age-groups/blob/main/notebooks/experiments_plots.ipynb))
## Usage

### Initialization

Install requirements:<br>
`pip install -r requirements.txt`

### Run the project

Experiments can be run by executing the `main.py` as in `python src/main.py`.
In the 'main' code you can find the definition of the costants, the initial conditions and the model parameters. You can change all of them to compute ODEs and run different experiments (for example different vaccination strategies), based on your interests. If you want to analyze the results only for one vaccination strategy, you can comment the code section `FUNCTION CALL WITH COMBINATION OF VACCINATION STRATEGIES`, otherwise the previous one in the code. Then, you can comment or uncomment the plotting function calls to show certain graphs instead of others.

## Directory structure (only main elements)
```
SIRVSD-model-with-age-groups
  │── src
  │    │── main.py                                  # main script to run experiments
  │    │── plot_result.py                           # contains utility functions for plotting
  │    └── sirvd_solver.py                          # wrapper function to compute ODEs using different APIs
  │── notebooks
  │    │── experiments_plots.ipynb                  # notebook showing experimental results with qualitative analysis
  │    └── Multi-age structured SIRVSD.ipynb        # notebook showing the description of the model and the main code for computing ODEs 
  └── plots
      │── no_vaccination                            # folder contains different plots with no vaccination strategy
      │── strategy_comparison                       # folder contains different plots to compare vaccination strategies
      │── vaccination_strategy_ascending_order      # folder contains different plots starting from the vaccinations of the youngest
      │── vaccination_strategy_descending_order     # folder contains different plots starting from the vaccinations of the elderly
      │── vaccination_strategy_same_time            # folder contains different plots vaccinating all age groups at the same time
      └── SIRVSD_transition_schema.jpg              # transition schema of the model between compartments 

