import matplotlib.pyplot as plt


class Solver:
    def __init__(self, model_data):
        self.coords = model_data.get_coords()
        self.plot_args = model_data.get_plot_args()
        self.fig_parameters = model_data.get_fig_parms()
    

    def run_solve(self, output_path):
        plt.plot(*self.coords, 
                 marker=self.plot_args['marker']['value'],
                 color=self.plot_args['color']['value'],
                 ms=self.plot_args['ms']['value'],
                 label=self.plot_args['label']['value'])

        if 'grid' in self.fig_parameters:
            plt.grid()
        if 'label' in self.plot_args:
            plt.legend()
        if 'title' in self.fig_parameters:
            plt.title(self.fig_parameters['title']['value'])
        
        plt.savefig(f'{output_path}/result.png')

