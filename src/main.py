#imports
from parser import Parser
from solver import Solver
from handler import Handler


def run(data, output_path):
    parser = Parser(3)
    init_data_path = parser.get_hdf5()
    solver = Solver(init_data_path)
    result_data_path = solver.run()
    handler = Handler(result_data_path, output_path)
    handler.get_graphical_output(parser.get_user_graphical_data())
    

if __name__ == '__main__':
    run(data='./../test/data.json', output_path='./../test/result_solver_data')
