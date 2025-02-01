from . import validator

def run_validator(data_path):
    valid = validator.Validator(data_path)
    valid.date_examination()
    valid.start_time_examination()

if __name__=='__main__':
    run_validator('src/data.json') 