#include <stdio.h>
#include <vector>
#include <omp.h>
#include <cmath>
#include <fstream>
#include <iomanip>

const int N = 25000;
const double TOL = 1e-6;
const int MAX_ITER = 1000;

void init(std::vector<double>& A, std::vector<double>& b) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++)
            A[i * N + j] = (i == j) ? 2.0 : 1.0;
        b[i] = N + 1.0;
    }
}

double norm(const std::vector<double>& x1, const std::vector<double>& x2) {
    double max = 0.0;
    for (int i = 0; i < N; i++) {
        double d = fabs(x1[i] - x2[i]);
        if (d > max) max = d;
    }
    return max;
}

double solve_v1(const std::vector<double>& A, const std::vector<double>& b, int threads) {
    std::vector<double> x(N, 0.0);
    std::vector<double> x_new(N, 0.0);
    
    omp_set_num_threads(threads);
    double t0 = omp_get_wtime();
    
    for (int iter = 0; iter < MAX_ITER; iter++) {
        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            double sum = 0.0;
            for (int j = 0; j < N; j++)
                if (i != j) sum += A[i * N + j] * x[j];
            x_new[i] = (b[i] - sum) / A[i * N + i];
        }
        
        #pragma omp parallel for
        for (int i = 0; i < N; i++)
            x[i] = x_new[i];
        
        if (norm(x, x_new) < TOL) break;
    }
    
    double t1 = omp_get_wtime();
    return t1 - t0;
}

double solve_v2(const std::vector<double>& A, const std::vector<double>& b, int threads) {
    std::vector<double> x(N, 0.0);
    std::vector<double> x_new(N, 0.0);
    
    omp_set_num_threads(threads);
    double t0 = omp_get_wtime();
    
    #pragma omp parallel
    {
        for (int iter = 0; iter < MAX_ITER; iter++) {
            #pragma omp for
            for (int i = 0; i < N; i++) {
                double sum = 0.0;
                for (int j = 0; j < N; j++)
                    if (i != j) sum += A[i * N + j] * x[j];
                x_new[i] = (b[i] - sum) / A[i * N + i];
            }
            
            #pragma omp for
            for (int i = 0; i < N; i++)
                x[i] = x_new[i];
            
            int done = 0;
            #pragma omp single
            {
                if (norm(x, x_new) < TOL) {
                    done = 1;
                }
            }
            if (done) break;
        }
    }
    
    double t1 = omp_get_wtime();
    return t1 - t0;
}

int main() {
    int threads[] = {1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40};
    int n_threads = sizeof(threads) / sizeof(threads[0]);
    
    std::vector<double> A(N * N);
    std::vector<double> b(N);
    
    printf("Initializing %dx%d matrix...\n", N, N);
    init(A, b);
    printf("Done.\n\n");
    
    std::ofstream file("speedup_data.txt");
    file << std::fixed << std::setprecision(6);
    file << "# N = " << N << "\n";
    
    // Version 1
    printf("=== VERSION 1 ===\n");
    double t1 = solve_v1(A, b, 1);
    printf("p=1: %.4fs\n", t1);
    file << "# Version 1\n# Threads Time Speedup\n";
    file << "1 " << t1 << " 1.0000\n";
    
    for (int i = 1; i < n_threads; i++) {
        double tp = solve_v1(A, b, threads[i]);
        double speedup = t1 / tp;
        printf("p=%2d: %.4fs (S=%.3f)\n", threads[i], tp, speedup);
        file << threads[i] << " " << tp << " " << speedup << "\n";
    }
    
    // Version 2
    printf("\n=== VERSION 2 ===\n");
    double t2 = solve_v2(A, b, 1);
    printf("p=1: %.4fs\n", t2);
    file << "\n# Version 2\n# Threads Time Speedup\n";
    file << "1 " << t2 << " 1.0000\n";
    
    for (int i = 1; i < n_threads; i++) {
        double tp = solve_v2(A, b, threads[i]);
        double speedup = t2 / tp;
        printf("p=%2d: %.4fs (S=%.3f)\n", threads[i], tp, speedup);
        file << threads[i] << " " << tp << " " << speedup << "\n";
    }
    
    file.close();
    
    printf("\nData saved to speedup_data.txt\n");
    return 0;
}