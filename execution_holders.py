import numpy as np

from sandSimulation import sand_simulation

def dimensions_square():
    type_string = "square"
    #dim = 30
    dim_list = range(20, 101, 20)
    strain_normal = 0.25
    strain_deviation = 0.15


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    for i in range(0, len(dim_list)):
        sand_simulation("squareDim/dim:{}".format(dim_list[i]), type_string, dim_list[i], strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor)



def dimensions_hex():
    type_string = "hex"
    #dim = 30
    dim_list = range(20, 101, 20)
    strain_normal = 0.25
    strain_deviation = 0.15


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    for i in range(0, len(dim_list)):
        sand_simulation("hexDim/dim:{}".format(dim_list[i]), type_string, dim_list[i], strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor)


def strain_deviation_hex():
    type_string = "hex"
    dim = 60
    strain_normal = 0.25
    #strain_deviation = 0.15
    strain_deviation_list = np.linspace(0, 0.5, 10, endpoint=True)
    print(strain_deviation_list)


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    for i in range(0, len(strain_deviation_list)):
        sand_simulation("hexStrain/strain:{:.2}".format(strain_deviation_list[i]).replace(".", ""), type_string, dim, strain_normal, strain_deviation_list[i], min_lambda, decrement_step_size, relax_iterations, mu, move_factor)

def strain_deviation_square():
    type_string = "square"
    dim = 60
    strain_normal = 0.25
    #strain_deviation = 0.15
    strain_deviation_list = np.linspace(0, 0.5, 10, endpoint=True)
    print(strain_deviation_list)


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    for i in range(0, len(strain_deviation_list)):
        sand_simulation("squareStrain/strain:{:.2}".format(strain_deviation_list[i]).replace(".", ""), type_string, dim, strain_normal, strain_deviation_list[i], min_lambda, decrement_step_size, relax_iterations, mu, move_factor)


def main():
    strain_deviation_square()

if __name__ == "__main__":
    main()
