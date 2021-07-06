import numpy as np
from scipy.integrate import odeint, solve_ivp

def sirvd_solver(t,beta_matrix,gamma,mu_group,phi, rho,eta_group,x0,start_vaccination):
    """Wrapper function to compute ODEs using different APIs (currently only with methods of SciPy)

    Args:
        t (np.ndarray): simulation time
        beta_matrix (np.ndarray): infection coefficient for each group
        gamma (float): recovery coefficient (same for all group)
        mu_group (list): mortality coefficient for each group (case fatality rate ISS report January 2021)
        phi (float): transfer coefficient for loss of immunity from recovered (six months of immunity and same for all group)
        rho (float): transfer coefficient for loss of immunity from vaccinated (nine months of immunity and same for all group)
        eta_group (list): vaccination coefficient for each group
        x0 (list): initial conditions
        start_vaccination (list): day of start of the vaccination period for each group
    """

    def assign_vaccination_coefficient(t, eta, start_vaccination):
        """Auxiliary function to assign time-dependent vaccination coefficient eta

        Args:
            t (float): scalar representing the current timestamp
            eta (float): vaccination coefficient
            start_vaccination (int): starting day of vaccination

        Returns:
            float: eta for a specific timestamp (0 or eta)
        """
        if t < start_vaccination or start_vaccination == -1: # -1 means no vaccination for a specific age group
            return 0
        else:
            return eta
    
    def sirvd(t,x,beta_matrix,gamma,mu_group,phi,rho,eta_group,start_vaccination,assign_vaccination_coefficient):
        """
        Function called by solve_ivp (or odeint) to compute the derivative of x at t.
        """
        n_groups = len(start_vaccination) # or any other "_group" parameter
        derivatives_matrix = np.zeros((5,4)) # save all derivatives in a 2-D array
        n_infectious = [x[j+n_groups] for j in range(0,n_groups)] # list of the number of infectious measured for each group
        for j in range(0,n_groups):
            s = x[j] # Susceptible
            # i = n_infectious[j]
            i = x[j+n_groups] # Infectious
            r = x[j+n_groups*2] # Recovered
            v = x[j+n_groups*3] # Vaccinated
            d = x[j+n_groups*4] # Deceased
            eta = assign_vaccination_coefficient(t,eta_group[j],start_vaccination[j]) # time-dependent parameter
            derivatives_matrix[0][j] = phi*r - eta*s + rho*v - s*np.dot(beta_matrix[j],n_infectious) # dsdt
            derivatives_matrix[1][j] = s*np.dot(beta_matrix[j],n_infectious) - gamma*i - mu_group[j]*i # didt
            derivatives_matrix[2][j] = gamma*i - phi*r # drdt
            derivatives_matrix[3][j] = eta*s - rho*v # dvdt
            derivatives_matrix[4][j] = mu_group[j]*i # dddt
        return derivatives_matrix.reshape(-1) # return all measurements with a 1-D array

    # odeint solve a system of ordinary differential equations using lsoda from the FORTRAN library odepack.
    # y = odeint(sirvd,x0,t,tfirst=True,args=(beta_matrix,gamma,mu_group,phi,rho,eta_group,start_vaccination,assign_vaccination_coefficient,))
    # return y
    # for new code, use scipy.integrate.solve_ivp to solve a differential equation (SciPy documentation).
    sol = solve_ivp(sirvd,[t[0],t[-1]],x0,t_eval=t,args=(beta_matrix,gamma,mu_group,phi,rho,eta_group,start_vaccination,assign_vaccination_coefficient,))
    return sol.y.T