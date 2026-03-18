#include <stdio.h>
#include <vector>
#include <fstream>
#include <iomanip>
#include <omp.h>


double wtime() {
    return omp_get_wtime();
}

void init_data(std::vector<double>& a, std::vector<double>& b, int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            a[i * n + j] = (i == j) ? 2.0 : 1.0;
        }
    }

    for (int i = 0; i < n; i++) {
        b[i] = 1.0;
    }
}

// void init_data(std::vector<double>& a, std::vector<double>& b, int m, int n) {
//     #pragma omp parallel for
//     for (int i = 0; i < m; i++) {
//         for (int j = 0; j < n; j++) {
//             a[i * n + j] = (i == j) ? 2.0 : 1.0;
//         }
//     }
//     #pragma omp parallel for
//     for (int i = 0; i < n; i++) {
//         b[i] = 1.0;
//     }
// }

void matrix_vector_product_omp(std::vector<double>& a, std::vector<double>& b, std::vector<double>& c, int m, int n) {
    #pragma omp parallel for
    for (int i = 0; i < m; i++) {
        c[i] = 0.0;
        for (int j = 0; j < n; j++) {
            c[i] += a[i * n + j] * b[j];
        }
    }
}

double run_parallel(int m, int n, int num_threads) {
    std::vector<double> a(m * n);
    std::vector<double> b(n);
    std::vector<double> c(m);
    
    init_data(a, b, m, n);
    omp_set_num_threads(num_threads);
    
    double t_start = wtime();
    matrix_vector_product_omp(a, b, c, m, n);
    double t_end = wtime();

    return t_end - t_start;
}

int main() {
    int sizes[] = {20000, 40000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    int threads[] = {1, 2, 4, 7, 8, 16, 20, 40};
    int num_tests = sizeof(threads) / sizeof(threads[0]);
    
    std::ofstream file("speedup_data.txt");    
    file << std::fixed << std::setprecision(6);
    
    for (int s = 0; s < num_sizes; s++) {
        int m = sizes[s];
        int n = sizes[s];
        
        // Замер для 1 потока
        double t1 = run_parallel(m, n, 1);
        printf("Size %d: T1 = %.4fs\n", m, t1);
        
        file << "# Size = " << m << "\n";
        file << "# Threads Time Speedup\n";
        
        for (int i = 0; i < num_tests; i++) {
            int p = threads[i];
            double tp = run_parallel(m, n, p);
            double speedup = (tp > 0.0) ? (t1 / tp) : 0.0;
            
            printf("  p=%2d: T=%.4fs S=%.3f\n", p, tp, speedup);
            file << p << " " << tp << " " << speedup << "\n";
        }
        file << "\n";
        printf("\n");
    }
    
    file.close();
    printf("Data saved to speedup_data.txt\n");
    return 0;
}