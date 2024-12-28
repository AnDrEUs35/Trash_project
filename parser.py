import json

class Parser:
    def __init__(self, data):
        with open(data) as data_file:
            self.data = json.load(data_file)
    

    def get_coords(self):
        coords = self.data['plot_data']
        return (coords['x_coords']['value'], 
                coords['y_coords']['value'])


    def get_plot_args(self):
        return self.data['plot_data']


    def get_fig_parms(self):
        return self.data['plot_data']