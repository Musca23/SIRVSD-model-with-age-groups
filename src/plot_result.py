import numpy as np
import matplotlib.pyplot as plt

# TODO define different plot functions
# TODO comment all methods

def plot_all_compartments_age_group(t, group_dict, results_dict, path):
    for group in group_dict:
        plt.figure(figsize=(20,5))
        plt.plot(t, results_dict[group][:, 0], 'g', label='S(t)')
        plt.plot(t, results_dict[group][:, 1], 'm', label='I(t)')
        plt.plot(t, results_dict[group][:, 2], 'r', label='R(t)')
        plt.plot(t, results_dict[group][:, 3], 'b', label='V(t)')
        plt.plot(t, results_dict[group][:, 4], 'k', label='D(t)')
        plt.legend(loc='best')
        plt.xticks(np.arange(t.min(), t.max()+1, 10))
        plt.yticks(np.arange(0, 1.005, 0.05))
        plt.xlabel('time')
        plt.ylabel('value')
        plt.title(group)
        plt.grid()
        # Saving the figure.
        plt.savefig(path+group+".jpg")
        plt.show()

def plot_all_compartments_entire_population(t, group_dict, results_dict, path, length_period):
        population = np.zeros((length_period, 5))
        for group in group_dict:
            population += results_dict[group]
        population = population/4 # values have to remain between 0 and 1
        plt.figure(figsize=(20,5))
        plt.plot(t, population[:, 0], 'g', label='S(t)')
        plt.plot(t, population[:, 1], 'm', label='I(t)')
        plt.plot(t, population[:, 2], 'r', label='R(t)')
        plt.plot(t, population[:, 3], 'b', label='V(t)')
        plt.plot(t, population[:, 4], 'k', label='D(t)')
        plt.legend(loc='best')
        plt.xticks(np.arange(t.min(), t.max()+1, 10))
        plt.yticks(np.arange(0, 1.005, 0.05))
        plt.xlabel('time')
        plt.ylabel('value')
        plt.title("Entire population")
        plt.grid()
        # Saving the figure.
        plt.savefig(path+".jpg")
        plt.show()

def plot_specific_compartment_all_age_group(t, group_dict, vacc_strategy, results_dict, path, compartment_id):
    plt.figure(figsize=(20,5))
    if compartment_id == 1: # Infectious
        comp_label = 'I(t)_'
        image_path = "/infectious_comparison.jpg"
        graph_title = "Infections comparison - "
    elif compartment_id == 4: # Deceased
        comp_label = 'D(t)_'
        image_path = "/deaths_comparison.jpg"
        graph_title = "Mortality comparison - "
    for group in group_dict:
        plt.plot(t, results_dict[vacc_strategy][group][:, compartment_id], label=comp_label+group)
    plt.legend(loc='best')
    plt.xticks(np.arange(t.min(), t.max()+1, 10))
    plt.yticks(np.arange(0, 1.005, 0.05))
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title(graph_title+vacc_strategy)
    plt.grid()
    # Saving the figure.
    plt.savefig(path+vacc_strategy+image_path)
    plt.show()

def plot_specific_compartment_compare_strategy(t, results_dict, path, compartment_id, length_period):
    population = {}
    if compartment_id == 1: # Infectious
        comp_label = 'I(t)_'
        graph_title = "Infections comparison - "
        image_path = "/infectious_comparison.jpg"
    elif compartment_id == 2: # Recovered
        comp_label = 'R(t)_'
        graph_title = "Recovery comparison - "
        image_path = "/recovered_comparison.jpg"
    elif compartment_id == 4: # Deceased
        comp_label = 'D(t)_'
        graph_title = "Mortality comparison - "
        image_path = "/deaths_comparison.jpg"
    for vacc_strategy, item_age_group in results_dict.items():
        population[vacc_strategy] = np.zeros((length_period))
        for age_group, values in item_age_group.items():
            population[vacc_strategy] += values[:, compartment_id]
        population[vacc_strategy] = population[vacc_strategy]/4 # values have to remain between 0 and 1
    # number_strategies = len(results_dict) # number of vaccination startegy
    plt.figure(figsize=(20,5))
    for vacc_strategy in results_dict:
        plt.plot(t, population[vacc_strategy], label=comp_label+vacc_strategy)
    plt.legend(loc='best')
    plt.xticks(np.arange(t.min(), t.max()+1, 10))
    plt.yticks(np.arange(0, 1.005, 0.05))
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title(graph_title+" entire population")
    plt.grid()
    # Saving the figure.
    plt.savefig(path+image_path+".jpg")
    plt.show()