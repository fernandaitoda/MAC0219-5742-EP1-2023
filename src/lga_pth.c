#include "lga_base.h"
#include "lga_pth.h"
#include <pthread.h>
#include <stdlib.h>

typedef struct
{
    byte *grid_in;
    byte *grid_out;
    int grid_size;
    int start_row;
    int end_row;
} ThreadArgs;

static byte get_next_cell(int i, int j, byte *grid_in, int grid_size)
{
    byte next_cell = EMPTY;

    for (int dir = 0; dir < NUM_DIRECTIONS; dir++)
    {
        int rev_dir = (dir + NUM_DIRECTIONS / 2) % NUM_DIRECTIONS;
        byte rev_dir_mask = 0x01 << rev_dir;

        int di = directions[i % 2][dir][0];
        int dj = directions[i % 2][dir][1];
        int n_i = i + di;
        int n_j = j + dj;

        if (inbounds(n_i, n_j, grid_size))
        {
            if (grid_in[ind2d(n_i, n_j)] == WALL)
            {
                next_cell |= from_wall_collision(i, j, grid_in, grid_size, dir);
            }
            else if (grid_in[ind2d(n_i, n_j)] & rev_dir_mask)
            {
                next_cell |= rev_dir_mask;
            }
        }
    }

    return check_particles_collision(next_cell);
}

static void *update(void *arg)
{
    ThreadArgs *args = (ThreadArgs *)arg;
    byte *grid_in = args->grid_in;
    byte *grid_out = args->grid_out;
    int grid_size = args->grid_size;
    int start_row = args->start_row;
    int end_row = args->end_row;
    
    for (int i = start_row; i < end_row; i++)
    {
        for (int j = 0; j < grid_size; j++)
        {
            if (grid_in[ind2d(i, j)] == WALL)
            {

                grid_out[ind2d(i, j)] = WALL;
            }
            else
            {
                grid_out[ind2d(i, j)] = get_next_cell(i, j, grid_in, grid_size);
            }
        }
    }

    pthread_exit(NULL);
}

void simulate_pth(byte *grid_1, byte *grid_2, int grid_size, int num_threads)
{
    pthread_t threads[num_threads];
    ThreadArgs thread_args[num_threads];

    int rows_per_thread = grid_size / num_threads;
    int remaining_rows = grid_size % num_threads;
    int current_row = 0;

    for (int i = 0; i < ITERATIONS / 2; i++)
    {
        for (int t = 0; t < num_threads; t++)
        {
            int start_row = current_row;
            int end_row = current_row + rows_per_thread;

            if (remaining_rows > 0)
            {
                end_row++;
                remaining_rows--;
            }

            current_row = end_row;

            thread_args[t].grid_in = grid_1;
            thread_args[t].grid_out = grid_2;
            thread_args[t].grid_size = grid_size;
            thread_args[t].start_row = start_row;
            thread_args[t].end_row = end_row;

            pthread_create(&threads[t], NULL, update, &thread_args[t]);
        }
        for (int t = 0; t < num_threads; t++)
        {
            pthread_join(threads[t], NULL);
        }

        byte *temp = grid_1;
        grid_1 = grid_2;
        grid_2 = temp;
    }

}
