from . import map_of_trash


def run(data, output_path):
    map_creating = map_of_trash.Map()
    map_creating.get_info_start(data)
    map_creating.get_info_end(data)
    map_creating.get_tracer((54.741906, -90.492995), 1000)
    #map_creating.get_map((54.741906, -90.492995), 1000)


if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
