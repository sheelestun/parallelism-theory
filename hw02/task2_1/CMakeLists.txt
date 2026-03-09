cmake_minimum_required(VERSION 3.10)
project(task2_1)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Найти OpenMP
find_package(OpenMP REQUIRED)

# Создать исполняемый файл
add_executable(test.out task2_1.cpp)

# Подключить OpenMP
target_link_libraries(test.out OpenMP::OpenMP_CXX)

# Оптимизации
target_compile_options(test.out PRIVATE -O3)

set_target_properties(test.out PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}
)