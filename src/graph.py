# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('resultados.csv')
data_sorted = data.sort_values(by=['Grid Size', 'Num Threads'])

grid_sizes = data_sorted['Grid Size'].unique()
num_threads = data_sorted['Num Threads'].unique()
implementations = data_sorted['Implementação'].unique()

mean_times = np.zeros((len(num_threads), len(grid_sizes), len(implementations)))
ci_times = np.zeros((len(num_threads), len(grid_sizes), len(implementations)))
for i, nt in enumerate(num_threads):
    for j, gs in enumerate(grid_sizes):
        for k, imp in enumerate(implementations):
            subset = data_sorted[(data_sorted['Grid Size'] == gs) & (data_sorted['Num Threads'] == nt) & (data_sorted['Implementação'] == imp)]
            measurements = subset[['Tempo 1', 'Tempo 2', 'Tempo 3', 'Tempo 4', 'Tempo 5', 'Tempo 6', 'Tempo 7', 'Tempo 8', 'Tempo 9', 'Tempo 10']]
            mean_times[i, j, k] = np.mean(measurements.values)
            ci_times[i, j, k] = 1.96 * np.std(measurements.values) / np.sqrt(len(measurements))


def media_e_IC():
# Função para gerar o gráfico de barras com intervalo de erro para cada implementação e número de threads
    def plot_error_bar_graph(impl, num_threads, grid_sizes, mean_times, ci_times):
        x = np.arange(len(grid_sizes))
        plt.figure(figsize=(10, 6))

        for i, nt in enumerate(num_threads):
            means = mean_times[i, :, impl]
            errors = ci_times[i, :, impl]
            plt.bar(x + i * 0.2, means, yerr=errors, capsize=5, width=0.2, align='center', alpha=0.7, label=f'Num Threads: {nt}')

        plt.xlabel('Tamanho da Grade')
        plt.ylabel('Tempo de Execução (s)')
        plt.title(f'Implementação: {implementations[impl]} - Média e Intervalo de Confiança')
        plt.xticks(x + 0.1 * len(num_threads), grid_sizes)
        plt.legend()
        plt.grid(True)

    for k, imp in enumerate(implementations):
        plot_error_bar_graph(k, num_threads, grid_sizes, mean_times, ci_times)

    plt.show()

def tempo_grade(): 
    # Gráfico de Linhas: Tempo de Execução em função do Tamanho da Grade
    plt.figure(figsize=(10, 6))
    
    for k, imp in enumerate(implementations):
        mean_times_by_threads = np.mean(mean_times[:, :, k], axis=0)
        plt.plot(grid_sizes, mean_times_by_threads, label=imp)
    
    plt.xlabel('Tamanho da Grade')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução em função do Tamanho da Grade')
    plt.legend()
    plt.grid(True)
    plt.show()

def tempo_threads():
    # Gráfico de Barras Agrupadas: Tempo de Execução em função do Número de Threads
    width = 0.2
    x = np.arange(len(num_threads))
    plt.figure(figsize=(10, 6))

    for k, imp in enumerate(implementations):
        mean_times_by_threads = np.mean(mean_times[:, :, k], axis=1)
        plt.bar(x + k * width, mean_times_by_threads, width=width, label=imp)

    plt.xlabel('Número de Threads')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução em função do Número de Threads')
    plt.xticks(x + width * len(implementations) / 2, num_threads)
    plt.legend()
    plt.grid(True)
    plt.show()

def tempo_grade_dispersao():
    execution_times = {}
    for imp in implementations:
        execution_times[imp] = {}
        for nt in num_threads:
            execution_times[imp][nt] = {}

    for gs in grid_sizes:
        for nt in num_threads:
            for imp in implementations:
                subset = data_sorted[(data_sorted['Grid Size'] == gs) & (data_sorted['Num Threads'] == nt) & (data_sorted['Implementação'] == imp)]
                execution_times[imp][nt][gs] = subset[['Tempo 1', 'Tempo 2', 'Tempo 3', 'Tempo 4', 'Tempo 5', 'Tempo 6', 'Tempo 7', 'Tempo 8', 'Tempo 9', 'Tempo 10']].values.flatten()

    def scatter_plots(impl):
        colors = plt.get_cmap('tab20', 8)
        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 6))

        axs.set_prop_cycle('color', [colors(i) for i in range(8)])
        for gs in grid_sizes:
            x = []
            y = []
            for nt in num_threads:
                x.extend([nt] * len(execution_times[impl][nt][gs]))
                y.extend(execution_times[impl][nt][gs])
            axs.scatter(x, y, label=f'Tamanho da Grade: {gs}', alpha=0.7)
        axs.set_xlabel('Número de Threads')
        axs.set_ylabel('Tempo de Execução (s)')
        axs.set_title(f'Implementação: {impl}')
        axs.legend()
        axs.grid(True)

    for implementation in implementations:
        scatter_plots(implementation)
    plt.tight_layout()
    plt.show()

def superficie():
# Função para gerar os gráficos de superfície para cada implementação
    def plot_surface_graph(impl, grid_sizes, num_threads, mean_times):
        X, Y = np.meshgrid(grid_sizes, num_threads)
        Z = mean_times[:, :, impl]

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k')
        ax.set_xlabel('Tamanho da Grade')
        ax.set_ylabel('Número de Threads')
        ax.set_zlabel('Tempo de Execução (s)')
        ax.set_title(f'Implementação: {implementations[impl]}')

    for k, imp in enumerate(implementations):
        plot_surface_graph(k, grid_sizes, num_threads, mean_times)

    plt.show()


def generate_graph(case):
    graphs = {
        1:media_e_IC,
        2:tempo_grade,
        3:tempo_threads,
        4:tempo_grade_dispersao,  
        5:superficie,
    }

    graphs.get(case, lambda:print("Opção inválida."))()
    
generate_graph(4)

