import solver
import parser
import sys 


def main(data_path: str=None, output_path: str=None) -> None:

    if data_path == None and output_path == None:
        _, data_path, output_path, *_ = sys.argv

    model_data = parser.Parser(data_path)
    model_solver = solver.Solver(model_data)
    model_solver.run_solve(output_path)


if __name__ == "__main__":
    main('./output.json', '.')
