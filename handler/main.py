from . import map_of_trash


def run(data, output_path):
    map_creating = map_of_trash.Map('./' + data)
    map_creating.get_info()
    map_creating.get_map((54.741906, -90.492995), 1)


if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
