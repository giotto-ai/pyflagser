cmake_minimum_required(VERSION 3.9)
project(flagser_pybind LANGUAGES CXX)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)

set(BINDINGS_DIR "src")

find_package(OpenMP)

pybind11_add_module(flagser_pybind "${BINDINGS_DIR}/flagser_bindings.cpp")
include_directories(.)
if(OpenMP_FOUND)
  target_link_libraries(flagser_pybind PRIVATE OpenMP::OpenMP_CXX)
endif()
target_compile_options(flagser_pybind PUBLIC -Ofast -DNDEBUG)
target_compile_options(flagser_pybind PUBLIC $<$<CONFIG:DEBUG>:-O2 -ggdb -D_GLIBCXX_DEBUG>)
# Cannot have two inlined namespace !
if(NOT CMAKE_BUILD_TYPE STREQUAL "Debug")
  target_compile_options(flagser_pybind PUBLIC -march=native -D_GLIBCXX_PARALLEL)
  target_link_libraries(flagser_pybind PRIVATE)
endif()
target_compile_definitions(flagser_pybind PRIVATE RETRIEVE_PERSISTENCE=1)
