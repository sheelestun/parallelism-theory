cmake_minimum_required(VERSION 3.10)
project(array_template)

set(CMAKE_CXX_STANDARD 11)

option(USE_FLOAT "Use float instead of double" OFF)

if(USE_FLOAT)
    add_definitions(-DUSE_FLOAT_TYPE)
endif()

add_executable(array_program.out task_1.cpp)