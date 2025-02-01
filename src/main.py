from parser import Parser


def run(data, output_path):
    parser = Parser(data, output_path)
    


if __name__ == "__main__":
    run(data= "./test/data.json", output_path="./test/result_solv_data")