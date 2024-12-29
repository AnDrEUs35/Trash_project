# FrontEnd
Здесь пока ничего нет, потому что я не понимаю, как я должен что-то здесь сделать,\
если не знаю **ничего** о том, что и в каком ***виде*** ко мне будет поступать...

## Это ужас
> Спасити, памагити

## Кусочек кода
'''python
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


'''