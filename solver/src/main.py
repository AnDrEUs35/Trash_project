#imports
from . import parser
from . import solver
from . import handler


def run(data, output_path):
    pars = parser.Parser( './' + data) #/workspaces/Trash_project/astro_data/data.json
    init_data_path = pars.get_hdf5(output_path)
    solve = solver.Solver(init_data_path)
    result_data_path = solve.run()
    handl = handler.Handler(result_data_path, output_path)
    handl.get_graphical_output(pars.get_user_graphical_data())
    pars.get_map((54.741906,20.492995), 200)
    

if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
