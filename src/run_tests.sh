#!/bin/bash


make clean
make

TIME_TEST_EXECUTABLE="./time_test"

grid_sizes="32 64 128 256 512 1024 2048 4096"

num_threads="1 2 4 8 16 32"

implementations="seq omp"

output_file="resultados.csv"

echo "Grid Size,Num Threads,Implementação,Tempo Médio" > $output_file

for grid_size in $grid_sizes; do
    for num_thread in $num_threads; do
        for impl in $implementations; do
            total_time=0

            # Executar o teste 10 vezes
            for ((i=1; i<=10; i++)); do
                result=$(LANG=C $TIME_TEST_EXECUTABLE --grid_size $grid_size --impl $impl --num_threads $num_thread)
                
                # Extrair o tempo da string result (supondo que o tempo seja a última palavra na string)
                # Certifique-se de que o formato do tempo seja consistente para a extração adequada.
                # Se o formato variar, adapte o comando abaixo para se ajustar ao formato específico.
                time=$(echo "$result" | awk '{print $NF}')

                # Somar o tempo total das 10 execuções
                total_time=$(awk "BEGIN {print $total_time + $time}")
            done

            # Calcular o tempo médio
            average_time=$(awk "BEGIN {print $total_time / 10}")

            # Adicionar a linha ao arquivo CSV
            echo "$grid_size,$num_thread,$impl,$average_time" >> $output_file
        done
    done
done

echo "Testes concluídos. Resultados salvos em $output_file."
