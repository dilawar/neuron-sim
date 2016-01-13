cmake_minimum_required(VERSION 2.6)

FIND_PACKAGE(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/../oc/
    ${CMAKE_CURRENT_SOURCE_DIR}/../nrnmpi
    )

SET(EXTERNAL_SRC_DIR
    ${CMAKE_CURRENT_SOURCE_DIR}/../../share/lib/python/neuron/rxd/geometry3d)
add_library(hoc MODULE inithoc.cpp)
add_library(graphicsPrimitive MODULE ${EXTERNAL_SRC_DIR}/graphicsPrimitives.cpp)
add_library(ctng MODULE ${EXTERNAL_SRC_DIR}/ctng.cpp)
add_library(surfaces MODULE ${EXTERNAL_SRC_DIR}/surfaces.cpp
    ${EXTERNAL_SRC_DIR}/marching_cubes2.c 
    ${EXTERNAL_SRC_DIR}/llgramarea.c
    )

target_link_libraries(
    hoc 
    nrnpython
    nrnhoc
    oc
    nrniv
    ivoc
    memacs
    meschach
    neuron_gnu
    nrnmpi
    scopmath
    sparse13
    sundails
    readline
    IVhines
    )
