import frontend.src.main as frontend
# import frontend.src.validator as validator


def run(config_path, output_path):
    frontend.run_validator(config_path)


if __name__ == "__main__":
    run('./test/frontend_output_bug.json', './')