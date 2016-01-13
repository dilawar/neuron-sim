cmake_minimum_required(VERSION 2.6)
FIND_PACKAGE(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/../oc/
    ${CMAKE_CURRENT_SOURCE_DIR}/../nrnmpi
    )
add_library(hoc MODULE inithoc.cpp)
