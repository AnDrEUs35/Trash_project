#imports
from . import parser
from . import solver
from . import handler


def run(data, output_path):
    parser = parser.Parser(data)
    init_data_path = parser.get_hdf5(output_path)
    solver = solver.Solver(init_data_path)
    result_data_path = solver.run()
    handler = handler.Handler(result_data_path, output_path)
    handler.get_graphical_output(parser.get_user_graphical_data())
    

if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
