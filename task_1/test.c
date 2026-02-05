#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define INIT_SIZE (int)pow(10, 7)
#define STEP 6.28 / INIT_SIZE

void fill_arrays_parallel(double *d_array, float *f_array, int size) {
    #pragma omp parallel
    {
        #pragma omp for
        for(int i = 0; i < size; i++) {
            double value = i * STEP;
            d_array[i] = value;
            f_array[i] = (float)value;
        }
    }
}

int main() {
    double *double_array = malloc(INIT_SIZE * sizeof(double));
    float *float_array = malloc(INIT_SIZE * sizeof(float));

    double start_time = omp_get_wtime();
    
    fill_arrays_parallel(double_array, float_array, INIT_SIZE);
    
    double end_time = omp_get_wtime();

    printf("%.3f\n", end_time - start_time);
    
    free(float_array);
    free(double_array);
    
    return 0;
}