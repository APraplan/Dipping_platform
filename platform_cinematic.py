import data_gestion as dg
import platform_coordinates as pc
import platform_move_functions as pmf


def run_dipping(file_name, sheet_name):

    glass_sample = dg.read_dipping_parameter(file_name, sheet_name)

    for n in range(len(glass_sample)):

        print('Dipping sample ', n, end='')

        pmf.take(glass_sample[n])

        pmf.dip_cycle(glass_sample[n], pc.solution1, pc.solution2, pc.clean_solution)

        pmf.store(glass_sample[n])

        print('Done')
