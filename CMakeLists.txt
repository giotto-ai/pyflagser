cmake_minimum_required(VERSION 3.9)
project(flagser_pybind LANGUAGES CXX)


add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)

set(BINDINGS_DIR "src")

find_package(OpenMP)

pybind11_add_module(flagser_pybind "${BINDINGS_DIR}/flagser_bindings.cpp")

if(OpenMP_FOUND)
  target_link_libraries(flagser_pybind PRIVATE OpenMP::OpenMP_CXX)
endif()

target_compile_definitions(flagser_pybind PRIVATE RETRIEVE_PERSISTENCE=1)
target_include_directories(flagser_pybind PRIVATE .)

if(MSVC)
    target_compile_options(flagser_pybind PUBLIC $<$<CONFIG:RELEASE>: /Wall /O2>)
    target_compile_options(flagser_pybind PUBLIC $<$<CONFIG:DEBUG>:/O1 /DEBUG:FULL /Zi /Zo>)
else()
    target_compile_options(flagser_pybind PUBLIC $<$<CONFIG:RELEASE>: -Ofast>)
    target_compile_options(flagser_pybind PUBLIC $<$<CONFIG:DEBUG>: -O2 -ggdb -D_GLIBCXX_DEBUG>)
endif()
