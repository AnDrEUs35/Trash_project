from . import map_of_trash
import json
import os

def run(arepo, output_path, data):
    end_file = sorted(os.listdir(arepo))[-1]
    map_creating = map_of_trash.Map(output_path)
    map_creating.get_info_start(arepo + '/snap_000.hdf5')
    map_creating.get_info_end(arepo + f"/{end_file}")
    with open(data, 'r') as data_file:
        data = json.load(data_file)
        width, long, radius = data['main_settings']['WIDTH']['value'], data['main_settings']['LONG']['value'], data['main_settings']['RADIUS']['value']
    map_creating.get_tracer((width, long), radius)
    # map_creating.get_map((54.741906, -90.492995), 1000)


if __name__ == '__main__':
    run(data='/workspaces/Trash_project/test/data.json', output_path='./../test/result_solver_data')
