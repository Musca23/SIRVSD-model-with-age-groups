import numpy as np
import matplotlib.pyplot as plt
import math

# TODO define different plot functions
# TODO define number of individuals in each compartment at the end of the year with bar chart
# TODO check lab24 and rolling mean
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

def plot_all_compartments_entire_population(t, group_dict, results_dict, path, length_period, eradication = False):
        eradication_disease_day = None
        space_values_time = 10 # spacing between values
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
        if eradication:
            space_values_time = 30 # we expected the eradication of the disease after some years, so we study the curve month by month
            measurements = population[:, 1].T # transpose the measurements to work with a 1-D array
            for idx, x in np.ndenumerate(measurements):
                if x <= 1e-6: # very very little fraction of infectious w.r.t the whole population
                    eradication_disease_day = idx[0]
                    break
        plt.legend(loc='best')
        plt.xticks(np.arange(t.min(), t.max()+1, space_values_time))
        plt.yticks(np.arange(0, 1.005, 0.05))
        plt.xlabel('time')
        plt.ylabel('value')
        plt.title("Entire population")
        plt.grid()
        if eradication_disease_day is not None:
            plt.annotate('Eradication disease', xy=(eradication_disease_day, 0), xytext=(180, 0.85), arrowprops=dict(facecolor='black', arrowstyle='->'),)
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
    plt.savefig(path+image_path)
    plt.show()

def plot_pie_chart_zero_day(group_dict, vacc_strategy, results_dict, path, compartment_id, length_period):
    if compartment_id == 1: # Infectious
        comp_label = 'infections'
        image_path = "/zero_day_infection.jpg"
    elif compartment_id == 4: # Deceased
        comp_label = 'deaths'
        image_path = "/zero_day_deaths.jpg"
    zero_day = []
    population = np.zeros((length_period, 5))
    for group in group_dict:
        population += results_dict[group]
    population = population/4 # values have to remain between 0 and 1
    measurements = population[:, compartment_id].T # transpose the measurements for a specific compartment
    for idx, x in np.ndenumerate(measurements):
        if idx != 0 and math.isclose(x, measurements[idx[0]-1], abs_tol=0.00001):
            zero_day.append(idx[0])
    if zero_day: # check if we actually have a zero day (zero deaths or zero infections in one day)        
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Susceptible', 'Infectious', 'Recovered', 'Vaccinated', 'Deaceased'
        sizes = population[zero_day[0], :].reshape(-1) # plt.pie require an 1-D to suppress warnings
        explode = (0, 0, 0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        colors = ['g','m','r','b', 'c']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("'Zero Day' for "+comp_label+" with "+vacc_strategy+" (day "+str(zero_day[0])+") ")
        # Saving the figure.
        plt.savefig(path+vacc_strategy+image_path)
        plt.show()
