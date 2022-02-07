cmake_minimum_required(VERSION 3.2)

project(optimal-wordle)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -O3")

add_executable(optimal_wordle src/optimal_wordle.cxx)
