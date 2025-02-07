#imports
from . import graphica3D
from . import solver
from . import handler


def run(data, output_path):
    graph = graphica3D.Graphica3D(data)
    init_data_path = graph.get_hdf5(output_path)
    solve = solver.Solver(init_data_path)
    result_data_path = solve.run()
    handl = handler.Handler(result_data_path, output_path)
    handl.get_graphical_output(graph.get_user_graphical_data())


if __name__ == '__main__':
    run(data='/workspaces/Trash_project/astro_data/data.json', output_path='./../test/result_solver_data')
