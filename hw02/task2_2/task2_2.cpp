#include <stdio.h>
#include <cmath>
#include <omp.h>
#include <fstream>
#include <iomanip>

// double integrate_omp(double (*func)(double), double a, double b, int n)
// {
//     double h = (b - a) / n;
//     double sum = 0.0;
//     #pragma omp parallel
//     {
//         int nthreads = omp_get_num_threads();
//         int threadid = omp_get_thread_num();
//         int items_per_thread = n / nthreads;
//         int lb = threadid * items_per_thread;
//         int ub = (threadid == nthreads - 1) ? (n - 1) : (lb + items_per_thread - 1);
//         double sumloc = 0.0;

//         for (int i = lb; i <= ub; i++) {
//             sumloc = func(a + h * (i + 0.5));    
//         }

//         #pragma omp atomic
//         sum += sumloc;
//     }
//     sum *= h;
//     return sum;
// }

double func(double x){
    return exp(-x * x);
}

double integrate_omp(double (*func)(double), double a, double b, int n)
{
    double h = (b - a) / n;
    double sum = 0.0;
    
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        sum += func(a + h * (i + 0.5));
    }
    
    sum *= h;
    return sum;
}

int main(){
    double a = 0.0, b = 3.14;
    int nsteps = 40000000;
    int threads[] = {1, 2, 4, 7, 8, 16, 20, 40};
    int num_tests = sizeof(threads) / sizeof(threads[0]);

    std::ofstream file("speedup_data.txt");
    file << std::fixed << std::setprecision(6);    
    // Последовательный замер
    omp_set_num_threads(1);
    double t0 = omp_get_wtime();
    double ref = integrate_omp(func, a, b, nsteps);
    double t_seq = omp_get_wtime() - t0;
    
    
    printf("Sequential time: %.6f sec\n", t_seq);
    printf("Result: %.10f\n\n", ref);
    file << "# nsteps = " << nsteps << "\n";
    file << "# Threads Time Speedup\n";
    printf("Threads\tTime\t\tSpeedup\n");
    printf("-------------------------------\n");
    
    for (int i = 0; i < num_tests; i++) {
        int nth = threads[i];
        omp_set_num_threads(nth);
        
        double t1 = omp_get_wtime();
        double res = integrate_omp(func, a, b, nsteps);
        double dt = omp_get_wtime() - t1;
        double speedup = t_seq / dt;
        printf("%d\t%.6f\t%.4f\n", nth, dt, speedup);
        file << nth << " " << dt << " " << speedup << "\n";
    }
    file.close();
    
    printf("\nData saved to speedup_data.txt\n");
    return 0;
}