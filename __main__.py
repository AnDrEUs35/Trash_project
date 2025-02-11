import frontend.src.main as frontend
import astro_data.src.main as debris_data
import solver.src.main as solver
import handler.main as graph_handler


def main(config_path, output_path):
    # frontend.run_validator(config_path)
    astro_data_path = debris_data.run(config_path)
    # astro_data_path = './astro_data/data.json'
    solver.run('astro_data/data_output/data.json', output_path)
    # graph_handler.run('astro_data/data_output/data.json', output_path)


if __name__ == "__main__":
    main('./test/frontend_output.json', './test')
    # main(sys.argv[1], sys.argv[2])