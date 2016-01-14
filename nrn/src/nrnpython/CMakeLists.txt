cmake_minimum_required(VERSION 2.6)

FILE(GLOB NRNPYTHON_SRC "*.cpp")

if("${CMAKE_SIZEOF_VOID_P}" EQUAL "8")
    add_definitions(-DNRNHOSTCPU="x86_64")
else() 
    add_definitions(-DNRNHOSTCPU="i586")
endif()

FIND_PACKAGE(PythonInterp REQUIRED)
FIND_PACKAGE(PythonLibs REQUIRED)
add_definitions("-DUSE_PYTHON -fPIC")

configure_file( ${CMAKE_CURRENT_SOURCE_DIR}/nrnpython_config.h.in
    ${CMAKE_CURRENT_SOURCE_DIR}/nrnpython_config.h
    )

include_directories( "${CMAKE_CURRENT_SOURCE_DIR}" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../oc" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../ivos" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../nrniv" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../ivoc" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../nrnoc" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../gnu" )
include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../mesch" )
include_directories( ${NUMPY_INCLUDE_DIRS} )
include_directories( ${PYTHON_INCLUDE_DIRS} )
include_directories( ${IV_INCLUDE_DIRS} )

if(APPLE)
    include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../mac" )
elseif(WIN32)
    include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../mswin" )
else()
    include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/../.." )
endif(APPLE)

add_library(nrnpython ${NRNPYTHON_SRC})
