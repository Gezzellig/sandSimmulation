import numpy as np

from sandSimulation import sand_simulation


def dimensions():
    type_string = "hex"
    #dim = 30
    dim_list = range(10, 101, 10)
    strain_normal = 0.25
    strain_deviation = 0.15


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    for i in range(0, len(dim_list)):
        sand_simulation("hexDim/dim:{}".format(dim_list[i]), type_string, dim_list[i], strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor)


def move_factor_hex():
    type_string = "hex"
    dim = 60
    strain_normal = 0.25
    strain_deviation = 0.15


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    move_factor_list = np.linspace(0.05, 1, 20)
    for i in range(0, len(move_factor_list)):
        sand_simulation("moveFactorListingHex/movefactor:{:.2}".format(move_factor_list[i]), type_string, dim, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor_list[i])

def move_factor_square():
    type_string = "square"
    dim = 60
    strain_normal = 0.25
    strain_deviation = 0.15


    min_lambda = 0.75
    decrement_step_size = 0.025
    relax_iterations = 9
    mu = 0.005
    move_factor = 0.3
    move_factor_list = np.linspace(0.05, 1, 20)
    for i in range(0, len(move_factor_list)):
        sand_simulation("moveFactorListingSquare/movefactor:{:.2}".format(move_factor_list[i]), type_string, dim, strain_normal, strain_deviation, min_lambda, decrement_step_size, relax_iterations, mu, move_factor_list[i])


def main():
    move_factor_square()

if __name__ == "__main__":
    main()
