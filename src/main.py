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
    END = 700 # day of end of the observation period
    START_VACCINATION_GROUP = [0, 0, 0, 0] # day of start of the vaccination period

    # initial conditions
    S_0_GROUP = [0.99, 0.99, 0.99, 0.99] # Susceptible
    I_0_GROUP = [0.01, 0.01, 0.01, 0.01] # Infectious
    R_0_GROUP = [0, 0, 0, 0] # Recovered
    V_0_GROUP = [0, 0, 0, 0] # Vaccinated
    D_0_GROUP = [0, 0, 0, 0] # Deceased

    # model parameters
    beta_matrix = np.array([[0.05,0.01,0.04,0.008],[0.01,0.09,0.08,0.008],[0.04,0.08,0.1,0.02],[0.008,0.008,0.02,0.03]]) # infection coefficient for each group
    gamma = 1/15 # recovery coefficient (same for all group)
    mu_group = [0.00009, 0.00005, 0.00688, 0.15987] # mortality coefficient for each group (case fataly rate ISS report January 2021)
    phi = 1/180 # transfer rate for loss of immunity from recovered (six months of immunity and same for all group)
    rho = 1/270 # transfer rate for loss of immunity from vaccinated (nine months of immunity and same for all group)
    eta_group = [0.0025, 0.0025, 0.0025, 0.0025] # vaccination rate for each group

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

    # ----- No vaccination -----
    # path = "./plots/no_vaccination/all_compartments_" # all compartments for each age group
    # plt.plot_all_compartments_age_group(t, group_dict, results_dict, path)
    # path = "./plots/no_vaccination/all_compartments_entire_population" # entire population
    # plt.plot_all_compartments_entire_population(t, group_dict, results_dict, path)

    # ----- Vaccination strategy in ascending order -----
    # path = "./plots/vaccination_strategy_ascending_order/all_compartments_" # age groups in ascending order
    # plt.plot_all_compartments_age_group(t, group_dict, results_dict, path)
    # path = "./plots/vaccination_strategy_ascending_order/all_compartments_entire_population" # entire population
    # plt.plot_all_compartments_entire_population(t, group_dict, results_dict, path)

    # ----- Vaccination strategy in descending order -----
    # path = "./plots/vaccination_strategy_descending_order/all_compartments_" # age groups in descending order
    # plt.plot_all_compartments_age_group(t, group_dict, results_dict, path)
    # path = "./plots/vaccination_strategy_descending_order/all_compartments_entire_population" # entire population
    # plt.plot_all_compartments_entire_population(t, group_dict, results_dict, path)

    # ----- Vaccination strategy at the same time -----
    # path = "./plots/vaccination_strategy_same_time/all_compartments_" # age groups at the same time
    # plt.plot_all_compartments_age_group(t, group_dict, results_dict, path)
    # path = "./plots/vaccination_strategy_same_time/all_compartments_entire_population" # entire population
    # plt.plot_all_compartments_entire_population(t, group_dict, results_dict, path)