import numpy as np
import matplotlib.pyplot as plt

# TODO define different plot functions

def plot_all_compartments_age_group(t, group_dict, results_dict):
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
        plt.title('Plotting results for '+group)
        plt.grid()
        # Saving the figure.
        # plt.savefig("./plots/output_"+group+".jpg")
        plt.show()
