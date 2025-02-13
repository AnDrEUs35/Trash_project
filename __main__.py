import frontend.src.main as frontend
import astro_data.src.main as debris_data
import solver.src.main as solver
import handler.main as graph_handler


def main(config_path, output_path):
    frontend.run_validator(config_path)
    debris_data_path = debris_data.run(config_path)
    solver.run(debris_data_path, output_path)

    arepo_output_path = './test'
    graph_handler.run(arepo_output_path, output_path)


if __name__ == "__main__":
    main('./test/frontend_output.json', './test')
    # main(sys.argv[1], sys.argv[2])