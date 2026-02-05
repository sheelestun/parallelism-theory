#include <iostream>
#include <cmath>

const int INIT_SIZE = 10000000;
const double STEP = 6.28 / INIT_SIZE;

int main() {
#ifdef USE_FLOAT_TYPE
    std::cout << "Using float type\n";
    float* array = new float[INIT_SIZE];
    
    for(int i = 0; i < INIT_SIZE; i++) {
        array[i] = static_cast<float>(i * STEP);
    }
#else
    std::cout << "Using double type\n";
    double* array = new double[INIT_SIZE];
    
    for(int i = 0; i < INIT_SIZE; i++) {
        array[i] = i * STEP;
    }
#endif
    
    std::cout << "First 5 elements: ";
    for(int i = 0; i < 5; i++) {
        std::cout << array[i] << " ";
    }
    std::cout << "\n";
    
    delete[] array;
    return 0;
}