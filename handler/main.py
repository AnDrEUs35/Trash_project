from . import map_of_trash


def run(data, output_path):
    map_creating = map_of_trash.Map(output_path)
    map_creating.get_info_start(data + '/snap_000.hdf5')
    map_creating.get_info_end(data + '/snap_058.hdf5')
    map_creating.get_tracer((29.741906, 60.492995), 300)
    map_creating.get_map((29.741906, 60.492995), 300)


if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
