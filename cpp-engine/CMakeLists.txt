cmake_minimum_required(VERSION 3.16)
project(KAVACH VERSION 3.3.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE Release)
add_compile_options(-O3 -march=native -flto -funroll-loops)

find_package(Threads REQUIRED)

add_executable(kavach src/main_kw.cpp)
target_include_directories(kavach PRIVATE include)
target_link_libraries(kavach PRIVATE Threads::Threads)

add_executable(aho_benchmark src/aho_benchmark.cpp)
target_include_directories(aho_benchmark PRIVATE include)
target_link_libraries(aho_benchmark PRIVATE Threads::Threads)
