#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

const double DOUBLE_INIT_SIZE = 10000000.0;
const double DOUBLE_STEP = static_cast<double> (6.28) / DOUBLE_INIT_SIZE;

const float FLOAT_INIT_SIZE = 10000000.0;
const float FLOAT_STEP = static_cast<float> (6.28) / FLOAT_INIT_SIZE;

int main() {
#ifdef USE_FLOAT_TYPE
    std::cout << "Using float type\n";
    std::vector<float> array (FLOAT_INIT_SIZE);
    
    for(int i = 0; i < (int)FLOAT_INIT_SIZE; i++) {
        array[i] = static_cast<float>(i) * FLOAT_STEP;
    }
    
    float sum_100 = 0.0f;
    std::cout << "First 100 elements: ";
    std::cout << std::fixed << std::setprecision(9);
    for(int i = 0; i < 100; i++) {
        std::cout << array[i] << " ";
        sum_100 += array[i];
    }
    std::cout << "\nSum of first 100 elements: " << sum_100 << "\n";
    
    float sum_total = 0.0f;
    for(int i = 0; i < (int)FLOAT_INIT_SIZE; i++) {
        sum_total += array[i];
    }
    double theoretical = 6.28 * (DOUBLE_INIT_SIZE - 1.0) / 2.0;
    std::cout << "Sum of all elements: " << std::setprecision(2) << sum_total << "\n";
#else
    std::cout << "Using double type\n";
    std::vector<double> array (DOUBLE_INIT_SIZE);
    for(int i = 0; i < (int)DOUBLE_INIT_SIZE; i++) {
        array[i] = static_cast<double>(i) * DOUBLE_STEP;
    }
    
    double sum_100 = 0.0;
    std::cout << "First 100 elements: ";
    std::cout << std::fixed << std::setprecision(9);
    for(int i = 0; i < 100; i++) {
        std::cout << array[i] << " ";
        sum_100 += array[i];
    }
    std::cout << "\nSum of first 100 elements: " << sum_100 << "\n";
    
    double sum_total = 0.0;
    for(int i = 0; i < (int)DOUBLE_INIT_SIZE; i++) {
        sum_total += array[i];
    }
    double theoretical = 6.28 * (DOUBLE_INIT_SIZE - 1.0) / 2.0;
    std::cout << "Sum of all elements: " << std::setprecision(2) << sum_total << "\n";
#endif
    
    return 0;
}