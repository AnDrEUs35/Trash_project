import frontend.src.main as front
import astro_data.src.main as debris_data
import solver.src.main as solve

def run(config_path, output_path):
    # front.run_validator(config_path)
    # data_path = debris_data.run(config_path)
    deta_path = 'astro_data/data.json'
    solve.run(deta_path, output_path)



if __name__ == "__main__":
    run('./astro_data/data.json', './test')