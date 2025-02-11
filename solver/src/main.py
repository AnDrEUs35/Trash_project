#imports
from . import parser
from . import solver
from . import handler
from . import map_of_trash


def run(data, output_path):
    pars = parser.Parser( './' + data) #/workspaces/Trash_project/astro_data/data.json
    init_data_path = pars.get_hdf5(output_path)
    solve = solver.Solver(init_data_path)
    result_data_path = solve.run()
    handl = handler.Handler(result_data_path, output_path)
    handl.get_graphical_output(pars.get_user_graphical_data())

    map_creating = map_of_trash.Map('/workspaces/Trash_project/IC.hdf5')
    map_creating.get_info_start()#вот сюда надо первый hdf5
    map_creating.get_info_end()#вот сюда надо последний hdf5
    map_creating.get_map((54.741906, -90.492995), 1000)
    map_creating.get_tracer((54.741906, -90.492995), 1000)



    

if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
