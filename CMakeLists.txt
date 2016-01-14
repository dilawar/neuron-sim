CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules)

PROJECT(neuron)

if("${CMAKE_SIZEOF_VOID_P}" EQUAL "8")
    MESSAGE("++ 64 bit architecture") 
    set(LDPREFIX "x86_64") 
else() 
    MESSAGE("++ 32 bit architecture") 
    unset(LDPREFIX)
endif()
add_definitions( -DUSE_PYTHON ) 


#if(LDPREFIX)
    #SET(NRN_LD_FLAGS "-L${NRN_INSTALL_DIR}/${LDPREFIX}/lib64")
#else()
    #SET(NRN_LD_FLAGS "-L${NRN_INSTALL_DIR}/lib")
#endif()
#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${NRN_LD_FLAGS}")

FIND_PACKAGE(PythonInterp REQUIRED)
FIND_PACKAGE(PythonLibs REQUIRED)
FIND_PACKAGE(NumPy REQUIRED)


SET(NRNPYTHON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/nrnpython)
SET(IV_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/iv)
SET(EXTERNAL_SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nrn/share/lib/python/neuron/rxd/geometry3d)
SET(NRN_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nrn)
SET(Python_ADDITIONAL_VERSIONS 2.7 2.6 3.3)

include_directories( ${IV_INSTALL_DIR}/include )
include_directories( ${PYTHON_INCLUDE_DIRS} )
include_directories( ${NUMPY_INCLUDES} )
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/oc/
    ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/nrnmpi
    )


SET(IV_INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/_iv)
add_custom_target(iv  ALL
    DEPENDS ${IV_INSTALL_DIR}/include/ivversion.h
    )

FILE(MAKE_DIRECTORY ${IV_INSTALL_DIR})
add_custom_command(OUTPUT ${IV_INSTALL_DIR}/include/ivversion.h
    COMMAND ./build.sh
    COMMAND ./configure  --prefix ${IV_INSTALL_DIR}
    COMMAND $(MAKE) 
    COMMAND make install
    WORKING_DIRECTORY ${IV_SOURCE_DIR}
    VERBATIM
    )
LINK_DIRECTORIES( ${IV_INSTALL_DIR}/${LDPREFIX}/lib 
    ${IV_INSTALL_DIR}/${LDPREFIX}/lib64
    )
SET(IV_INCLUDE_DIRS ${IV_INSTALL_DIR}/include)
include_directories( ${IV_INCLUDE_DIRS} )


##
#### Target to build nrnpython library.
##SET(NRNPYTHON_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/_nrnpython)
##FILE(MAKE_DIRECTORY ${NRNPYTHON_BUILD_DIR})
##add_custom_target(neuronpython ALL
##    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/libnrnpython.so
##    )
##add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/libnrnpython.so 
##    COMMAND ${CMAKE_COMMAND}  -DIV_INCLUDE_DIRS=${IV_INCLUDE_DIRS}
##        ${NRN_SOURCE_DIR}/src/nrnpython
##    COMMAND $(MAKE)
##    WORKING_DIRECTORY ${NRNPYTHON_BUILD_DIR}
##    )
##
## Convert cython files to cpp files.
##FIND_PACKAGE(Cython REQUIRED)
##FILE(GLOB CYTHON_SRC "${EXTERNAL_SRC_DIR}/*.pyx")
##foreach( CYFILE ${CYTHON_SRC})
##    MESSAGE(STATUS "Generating ${CYFILE}.cpp from ${CYFILE}")
##    execute_process(
##        COMMAND ${CYTHON_EXECUTABLE} ${CYFILE} -o ${CYFILE}.cpp
##        )
##endforeach()

## Generate parse.h using bison
FIND_PACKAGE(BISON REQUIRED)

MESSAGE(STATUS "Using ${PYTHON_EXECUTABLE}")
SET(NRN_INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/_nrn)
LINK_DIRECTORIES( ${NRN_INSTALL_DIR}/${LDPREFIX}/lib
    ${NRN_INSTALL_DIR}/${LDPREFIX}/lib64 
    )

FILE(MAKE_DIRECTORY ${NRN_INSTALL_DIR})

add_custom_target(nrn  ALL
    DEPENDS ${NRN_INSTALL_DIR}/${LDPREFIX}/bin/nrniv
    )

add_custom_command(OUTPUT ${NRN_INSTALL_DIR}/${LDPREFIX}/bin/nrniv
    COMMAND ./build.sh 
    COMMAND ./configure --with-iv=${IV_INSTALL_DIR} --with-nrnpython --prefix ${NRN_INSTALL_DIR} --with-x  --disable-rpath
    COMMAND $(MAKE) 
    COMMAND make install
    WORKING_DIRECTORY ${NRN_SOURCE_DIR}
    VERBATIM
    )

add_library(hoc MODULE ${NRNPYTHON_DIR}/inithoc.cpp)

configure_file( ${NRNPYTHON_DIR}/setup_cmake.py.in
    ${NRNPYTHON_DIR}/setup_cmake.py
    )

configure_file( ${NRN_SOURCE_DIR}/src/oc/nrnmpiuse.h.in
    ${NRN_SOURCE_DIR}/src/oc/nrnmpiuse.h
    )
configure_file( ${NRN_SOURCE_DIR}/src/oc/nrnpthread.h.in
    ${NRN_SOURCE_DIR}/src/oc/nrnpthread.h
    )

## Build

set_target_properties(hoc
    PROPERTIES PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY ${NRNPYTHON_DIR}/neuron
    )

add_library(graphicsPrimitives MODULE
    ${EXTERNAL_SRC_DIR}/graphicsPrimitives.pyx.cpp
    )

set_target_properties(graphicsPrimitives
    PROPERTIES PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY ${NRNPYTHON_DIR}/neuron/rxd/geometry3d
    )

add_library(ctng MODULE ${EXTERNAL_SRC_DIR}/ctng.pyx.cpp
    )
set_target_properties(ctng 
    PROPERTIES PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY ${NRNPYTHON_DIR}/neuron/rxd/geometry3d/surfaces
    )
add_library(surfaces MODULE ${EXTERNAL_SRC_DIR}/surfaces.pyx.cpp
    ${EXTERNAL_SRC_DIR}/marching_cubes2.c 
    ${EXTERNAL_SRC_DIR}/llgramarea.c
    )
set_target_properties(surfaces
    PROPERTIES PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY ${NRNPYTHON_DIR}/neuron/rxd/geometry3d/surfaces
    )

target_link_libraries(hoc 
    nrnoc
    oc
    nrniv
    ivoc
    memacs
    meschach
    neuron_gnu
    nrnmpi
    scopmath
    sparse13
    sundials
    readline
    IVhines
    nrnpython
    )


FIND_PACKAGE(PythonInterp REQUIRED)

add_dependencies(nrn iv)
add_dependencies(hoc nrn)

# install
install(DIRECTORY ${NRN_INSTALL_DIR}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    )

install(DIRECTORY ${IV_INSTALL_DIR}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    )

install(CODE
    "
    EXECUTE_PROCESS(
        COMMAND
        ${PYTHON_EXECUTABLE} setup_cmake.py install -v --prefix ${CMAKE_INSTALL_PREFIX}
        RESULT_VARIABLE NRNPYTHON_INSTALL_RESULT
        WORKING_DIRECTORY ${NRN_SOURCE_DIR}/src/nrnpython
    )
    MESSAGE(STATUS ${NRNPYTHON_INSTALL_RESULT})
    "
    )

