import frontend.src.main as frontend
import astro_data.src.main as debris_data


def run(config_path, output_path):
    frontend.run_validator(config_path)
    # debris_data.run(config_path, output_path)


if __name__ == "__main__":
    run('./test/frontend_output.json', './test')