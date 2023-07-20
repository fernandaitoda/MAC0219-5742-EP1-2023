# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

# Leitura dos dados a partir do arquivo CSV
data = pd.read_csv('resultados.csv')

# Grupos de interesse para a análise (Grid Size e Num Threads)
grid_sizes = data['Grid Size'].unique()
num_threads = data['Num Threads'].unique()
implementations = data['Implementação'].unique()

# Cálculo do tempo médio e do intervalo de confiança para cada combinação de Grid Size e Num Threads
mean_times = np.zeros((len(num_threads), len(grid_sizes), len(implementations)))
ci_times = np.zeros((len(num_threads), len(grid_sizes), len(implementations)))
for i, nt in enumerate(num_threads):
    for j, gs in enumerate(grid_sizes):
        for k, imp in enumerate(implementations):
            subset = data[(data['Grid Size'] == gs) & (data['Num Threads'] == nt) & (data['Implementação'] == imp)]
            measurements = subset[['Tempo 1', 'Tempo 2', 'Tempo 3', 'Tempo 4', 'Tempo 5', 'Tempo 6', 'Tempo 7', 'Tempo 8', 'Tempo 9', 'Tempo 10']]
            mean_times[i, j, k] = np.mean(measurements.values)
            ci_times[i, j, k] = 1.96 * np.std(measurements.values) / np.sqrt(len(measurements))


def media_e_IC():
# Função para gerar o gráfico de barras com intervalo de erro para cada implementação e número de threads
    def plot_error_bar_graph(implementacao, num_threads, grid_sizes, mean_times, ci_times):
        x = np.arange(len(grid_sizes))
        plt.figure(figsize=(10, 6))

        # Obter índices que classificam os tamanhos de grade em ordem crescente
        sorted_indices = np.argsort(grid_sizes)

        for i, nt in enumerate(num_threads):
            means = mean_times[i, sorted_indices, implementacao]
            errors = ci_times[i, sorted_indices, implementacao]
            plt.bar(x + i * 0.2, means, yerr=errors, capsize=5, width=0.2, align='center', alpha=0.7, label=f'Num Threads: {nt}')

        # Obter os tamanhos de grade classificados em ordem crescente
        sorted_grid_sizes = np.array(grid_sizes)[sorted_indices]

        plt.xlabel('Tamanho da Grade')
        plt.ylabel('Tempo de Execução (s)')
        plt.title(f'Implementação: {implementations[implementacao]} - Média e Intervalo de Confiança')
        plt.xticks(x + 0.1 * len(num_threads), sorted_grid_sizes)
        plt.legend()
        plt.grid(True)

    # Para cada implementação, chame a função para gerar o gráfico de barras com intervalo de erro
    for k, imp in enumerate(implementations):
        plot_error_bar_graph(k, num_threads, grid_sizes, mean_times, ci_times)

    plt.show()








def tempo_grade(): 
# Gráfico de Linhas: Tempo de Execução em função do Tamanho da Grade
    plt.figure(figsize=(10, 6))
    for k, imp in enumerate(implementations):
        plt.plot(grid_sizes, mean_times[0, :, k], label=imp)
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
        plt.bar(x + k * width, mean_times[:, 0, k], width=width, label=imp)
    plt.xlabel('Número de Threads')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução em função do Número de Threads')
    plt.xticks(x + width * len(implementations) / 2, num_threads)
    plt.legend()
    plt.grid(True)
    plt.show()

def tempo_grade_barras():
# Gráfico de Barras Empilhadas: Comparação do Tempo de Execução para cada Tamanho de Grade
    width = 0.2
    x = np.arange(len(grid_sizes))
    plt.figure(figsize=(10, 6))
    for k, imp in enumerate(implementations):
        plt.bar(x, mean_times[0, :, k], yerr=ci_times[0, :, k], width=width, label=imp)
        x = x + width
    plt.xlabel('Tamanho da Grade')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Comparação do Tempo de Execução para cada Tamanho de Grade')
    plt.xticks(np.arange(len(grid_sizes)) + width * len(implementations) / 2, grid_sizes)
    plt.legend()
    plt.grid(True)
    plt.show()

def superficie():
# Função para gerar os gráficos de superfície para cada implementação
    def plot_surface_graph(implementacao, grid_sizes, num_threads, mean_times):
        X, Y = np.meshgrid(grid_sizes, num_threads)
        Z = mean_times[:, :, implementacao]

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k')
        ax.set_xlabel('Tamanho da Grade')
        ax.set_ylabel('Número de Threads')
        ax.set_zlabel('Tempo de Execução (s)')
        ax.set_title(f'Implementação: {implementations[implementacao]}')

    # Para cada implementação, chame a função para gerar o gráfico de superfície
    for k, imp in enumerate(implementations):
        plot_surface_graph(k, grid_sizes, num_threads, mean_times)

    plt.show()


def generate_graph(case):
    graphs = {
        1:media_e_IC,
        2:tempo_grade,
        3:tempo_threads,
        4:tempo_grade_barras,
        5:superficie,
    }

    graphs.get(case, lambda:print("Opção inválida."))()


generate_graph(3)

