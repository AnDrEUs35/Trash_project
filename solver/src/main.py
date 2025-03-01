#imports
from . import graphica3D


def run(data_path, output_path):
    graph = graphica3D.Graphica3D(data_path, output_path)
    init_data_path = graph.get_hdf5()


if __name__ == '__main__':
    run(data='/workspaces/Trash_project/astro_data/data.json', output_path='./../test/result_solver_data')
