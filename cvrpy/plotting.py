import numpy as np
import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def plot_convergence(convergences: list, size=(15, 7), axes=None):
        if axes is None:
            fig1, ax1 = plt.subplots(1, 1, figsize=size)
        else:
            ax1 = axes
        
        num_iterations = len(convergences[0])
        grouped_by_runs = np.matrix(convergences).transpose()

        means    = [ np.mean(it) for it in grouped_by_runs ]
        stds     = [ np.std(it) for it in grouped_by_runs ]
        std_up   = [ (means[i] + stds[i]) for i in range(num_iterations) ]
        std_down = [ (means[i] - stds[i]) for i in range(num_iterations) ]

        ax1.plot(means, color='blue')
        ax1.plot(std_up, color='red', linewidth=0.6)
        ax1.plot(std_down, color='red', linewidth=0.6)

        ax1.grid(axis='both', color='#999', linestyle=':')
        ax1.set(
            title='Média e Desvio Padrão do fitness durante as execuções',
            ylabel='Valor da função objetivo',
            xlabel='Iteração',
            xlim=(0, num_iterations))

        if axes is None: return fig1, ax1
        else: return ax1