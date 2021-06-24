import numpy as np
from sir_solver import sir_solver
import plot_result as plt

if __name__ == "__main__":

    # ---------- DEFINITION OF COSTANTS ----------

    group_dict = {
    "children": 0,
    "teenagers": 1,
    "adults": 2,
    "senior": 3
    }
    START = 0 # day of start of the observation period
    END = 365 # day of end of the observation period
    START_VACCINATION_GROUP = [0, 0, 0, 0] # day of start of the vaccination period

    # initial conditions
    S_0_GROUP = [0.99, 0.99, 0.99, 0.99] # Susceptible
    I_0_GROUP = [0.01, 0.01, 0.01, 0.01] # Infectious
    R_0_GROUP = [0, 0, 0, 0] # Recovered
    V_0_GROUP = [0, 0, 0, 0] # Vaccinated
    D_0_GROUP = [0, 0, 0, 0] # Deceased

    # model parameters
    beta_matrix = np.array([[0.1,0.04,0.07,0.02],[0.04,0.1,0.09,0.02],[0.07,0.09,0.3,0.08],[0.02,0.02,0.08,0.08]]) # infection coefficient for each group TODO find the best values
    gamma = 1/15 # recovery coefficient (same for all group)
    mu_group = [0.00009, 0.00005, 0.00688, 0.15987] # mortality coefficient for each group (case fataly rate ISS report January 2021)
    phi = 1/180 # transfer rate for loss of immunity from recovered (six months of immunity and same for all group)
    rho = 1/270 # transfer rate for loss of immunity from vaccinated (nine months of immunity and same for all group)
    eta_group = [0.01, 0.01, 0.01, 0.01] # vaccination rate for each group TODO find the best values

    t = np.linspace(START,END,END-START+1) # setting the simulation time and the number of points

    # ---------- FUNCTION CALL ----------

    results_dict = {}
    x_0 = [*S_0_GROUP, *I_0_GROUP, *R_0_GROUP, *V_0_GROUP, *D_0_GROUP] # unpacking list operator
    y = sir_solver(t, beta_matrix, gamma, mu_group, phi, rho, eta_group, x_0, START_VACCINATION_GROUP)
    _, n_total_column = y.shape
    n_groups = len(group_dict) # number of age groups
    n_compartments = int(n_total_column/n_groups) # number of compartments of the model
    for group_name, group_id in group_dict.items():
        # select the right columns (the compartments) for each age group 
        results_dict[group_name] = y[:,[group_id+n_groups*j for j in range(0,n_compartments)]]

    # ---------- PLOT RESULTS ----------

    plt.plot_all_compartments_age_group(t, group_dict, results_dict)