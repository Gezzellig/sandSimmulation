import numpy as np

from plot import plot_all_strings_against_time, show_plot
from sandSimulation import sand_simulation
import multiprocessing
from functools import partial

class Run_settings:
    def __init__(self, folder_name, type_string, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor):
        self.folder_name = folder_name
        self.type_string = type_string
        self.dim = dim
        self.springconstant_normal = springconstant_normal
        self.springconstant_deviation = springconstant_deviation
        self.strain_normal = strain_normal
        self.strain_deviation = strain_deviation
        self.min_lambda = min_lambda
        self.decrement_step_size = decrement_step_size
        self.relax_iterations = relax_iterations
        self.mu = mu
        self.move_factor = move_factor


def sand_simulation_wrapper(rs):
    return sand_simulation(rs.folder_name, rs.type_string, rs.dim, rs.springconstant_normal, rs.springconstant_deviation, rs.strain_normal, rs.strain_deviation, rs.min_lambda, rs.decrement_step_size, rs.relax_iterations, rs.mu, rs.move_factor)


def execute_multi_process_with_plot(all_run_settings, legend_title, alternating_values, base_folder_name):
    all_grids = list()
    for rs in all_run_settings:
        all_grids.append(sand_simulation_wrapper(rs))
    #pool = multiprocessing.Pool()
    #all_grids = pool.map(sand_simulation_wrapper, all_run_settings)
    #plot_all_strings_against_time(all_grids, legend_title, alternating_values, base_folder_name)
    #show_plot()


def dimensions(type_string):
    #dim = 30
    dim_list = range(20, 101, 20)
    springconstant_normal = 1.0
    springconstant_deviation = 0
    strain_normal = 0.25
    strain_deviation = 0.15


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3

    all_run_settings = list()
    for i in range(0, len(dim_list)):
        all_run_settings.append(Run_settings("{}RanDim/dim:{}".format(type_string, dim_list[i]), type_string, dim_list[i], springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor))

    pool = multiprocessing.Pool()
    pool.map(sand_simulation_wrapper, all_run_settings)

def strain_deviation(type_string):
    dim = 60
    springconstant_normal = 1.0
    springconstant_deviation = 0
    strain_normal = 0.25
    #strain_deviation = 0.15
    strain_deviation_list = np.linspace(0, 0.5, 5, endpoint=True)

    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3

    all_run_settings = list()
    base_folder_name = "{}straindeviation".format(type_string)
    for i in range(0, len(strain_deviation_list)):
        all_run_settings.append(Run_settings("{}/springdeviation:{:.2}".format(base_folder_name, strain_deviation_list[i]).replace(".", ""), type_string, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation_list[i], min_lambda, decrement_step_size, relax_iterations, mu, move_factor))

    legend_title = "strain deviation"

    execute_multi_process_with_plot(all_run_settings, legend_title, strain_deviation_list, base_folder_name)


def springconstant_deviation(type_string):
    dim = 60
    springconstant_normal = 1.0
    #springconstant_deviation = 0
    springconstant_deviation_list = np.linspace(0, 0.5, 5, endpoint=True)
    strain_normal = 0.25
    strain_deviation = 0.0

    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3

    all_run_settings = list()
    base_folder_name = "{}Springdeviation".format(type_string)
    for i in range(0, len(springconstant_deviation_list)):
        all_run_settings.append(Run_settings("{}/springdeviation:{:.2}".format(base_folder_name, springconstant_deviation_list[i]).replace(".", ""), type_string, dim, springconstant_normal, springconstant_deviation_list[i], strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor))

    legend_title = "Springconstant deviation"

    execute_multi_process_with_plot(all_run_settings, legend_title, springconstant_deviation_list, base_folder_name)

def example(type_string):
    dim = 3
    springconstant_normal = 1.0
    springconstant_deviation = 0
    #springconstant_deviation_list = np.linspace(0, 0.5, 5, endpoint=True)
    strain_normal = 0.25
    strain_deviation = 0.15

    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 0
    mu = 0.005
    move_factor = 0.3

    all_run_settings = list()
    base_folder_name = "{}example".format(type_string)
    for i in range(0, 1):
        all_run_settings.append(Run_settings("{}/example2".format(base_folder_name).replace(".", ""), type_string, dim, springconstant_normal, springconstant_deviation, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor))

    legend_title = "Springconstant deviation"

    execute_multi_process_with_plot(all_run_settings, legend_title, list(), base_folder_name)

def main():
    hex = "hex"
    square = "square"
    example(hex)

if __name__ == "__main__":
    main()
