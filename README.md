# MAC0219-5742-EP1-2023

Você e seu grupo deverão paralelizar o código para a simulação do LGA usando a
biblioteca Pthreads e as diretivas de compilador fornecidas pelo OpenMP. Depois, vocês
deverão medir e comparar o tempo de execução das três versões: sequencial,
paralelizada com Pthreads e paralelizada com OpenMP.

Para compilar o projeto por completo, use o comando:
 
			$ make
      
Para compilar separadamente cada um dos executáveis, use os seguintes comandos:

      $ make check
      $ make time_test
      
Para testar se as implementações paralelas estão corretas, use o comando check:

      $ ./check ——grid_size <grid_size> ——num_threads <num_threads>
			
onde grid_size é o tamanho da entrada e num_threads é o número de threads.

Para medir o tempo de execução, use o comando time_test:

      $ ./time_test ——grid_size <grid_size> ——impl <impl> ——num_threads <num_threads>
			
onde impl é a versão do programa a ser executada (<impl> = seq, omp ou pth). No caso em que <impl> = seq, o argumento num_threads pode ser omitido (caso seja inserido, é ignorado).

Para remover os arquivos gerados na compilação, use o comando

      $ make clean

grid_size = 32, 64, 128, 256, 512, 1024, 2048, 4096
num_threads = 1, 2, 4, 8, 16, 32 (versões omp e pth)
impl = seq, omp, pth

Os arquivos lga_omp.c e lga_pth.c contém as versões paralelizadas do programa

Para rodar o script que gera o arquivo CSV com 10 medições para cada cado de execução:

      $ ./run_tests.sh
			
onde o arquivo de saída é resultados.csv

Para gerar os gráficos:

      $python3 graph.py
			
com  as seguintes bibliotecas python: numpy, matplotlib, pandas. (para instalar use pip install). 
OBS. cada execução da função gera um "grupo" de gráficos ou um gráfico seguindo a seguinte lógica que deve ser modificada: "generate_graph(NUMERO)", NUMERO = 1, 2, 3, 4, 5. 

      1:media_e_IC,
      2:tempo_grade,
      3:tempo_threads,
      4:tempo_grade_dispersao,  
      5:superficie,




