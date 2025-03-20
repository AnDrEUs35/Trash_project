import frontend.src.main as frontend
import astro_data.src.main as debris_data
import solver.src.main as solver
import handler.main as graph_handler
import sys
import os


def main(input_path, output_path, state):
    if state == 'config':
        config_path = input_path
        frontend.run_validator(config_path)
        debris_data_path = debris_data.run(config_path)
        solver.run(debris_data_path, output_path)
    elif state == 'handler':
        data = './test/frontend_output.json'
        arepo_output_path = input_path
        print('arepo output path: ', arepo_output_path)
        # for i in range(10):
        #     os.system(f'cp {arepo_output_path}/snap_00{i}.hdf5 {output_path}/snap_00{i}.hdf5')
        #     if i == range(10)[-1]:
        #         end_file = f'/snap_00{i}.hdf5'
        end_file = '/snap_040.hdf5'
        graph_handler.run(arepo_output_path, output_path, data, end_file)


if __name__ == "__main__":
    main('./test/frontend_output.json', './test', 'config')
    main('./test', './test', 'handler')
    # main(sys.argv[1], sys.argv[2], sys.argv[3])