cmake_minimum_required(VERSION 3.14)
project(slay_solver)

set(CMAKE_CXX_STANDARD 11)
find_package(OpenMP REQUIRED)

add_executable(test.out slay_solver.cpp)
target_link_libraries(test.out OpenMP::OpenMP_CXX)
target_compile_options(test.out PRIVATE -O3)

set_target_properties(test.out PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}
)