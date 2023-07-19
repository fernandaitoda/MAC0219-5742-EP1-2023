import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

# Gráfico de tempo de execução médio por tamanho da grade
plt.figure()
for i in range(len(num_threads)):
    for k, imp in enumerate(implementations):
        plt.errorbar(grid_sizes, mean_times[i, :, k], yerr=ci_times[i, :, k], label=f"{num_threads[i]} threads - {imp}", marker='o')

plt.xlabel("Tamanho da Grade")
plt.ylabel("Tempo de Execução Médio")
plt.title("Desempenho em relação ao Tamanho da Grade")
plt.legend()
plt.show()

# Gráfico de tempo de execução médio por número de threads e implementação
plt.figure()
for j in range(len(grid_sizes)):
    for k, imp in enumerate(implementations):
        plt.errorbar(num_threads, mean_times[:, j, k], yerr=ci_times[:, j, k], label=f"{grid_sizes[j]} grid size - {imp}", marker='o')

plt.xlabel("Número de Threads")
plt.ylabel("Tempo de Execução Médio")
plt.title("Desempenho em relação ao Número de Threads")
plt.legend()
plt.show()
