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


#if(LDPREFIX)
    #SET(NRN_LD_FLAGS "-L${NRN_INSTALL_DIR}/${LDPREFIX}/lib64")
#else()
    #SET(NRN_LD_FLAGS "-L${NRN_INSTALL_DIR}/lib")
#endif()
#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${NRN_LD_FLAGS}")

SET(IV_INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/_iv)
FILE(MAKE_DIRECTORY ${IV_INSTALL_DIR})
LINK_DIRECTORIES( ${IV_INSTALL_DIR}/${LDPREFIX}/lib )

SET(IV_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/iv)
add_custom_target(iv  ALL
    DEPENDS ${IV_INSTALL_DIR}/include/ivversion.h
    )

add_custom_command(OUTPUT ${IV_INSTALL_DIR}/include/ivversion.h
    COMMAND ./build.sh
    COMMAND ./configure  --prefix ${IV_INSTALL_DIR}
    COMMAND $(MAKE) 
    COMMAND make install
    WORKING_DIRECTORY ${IV_SOURCE_DIR}
    VERBATIM
    )

SET(NRN_INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/_nrn)
LINK_DIRECTORIES( ${NRN_INSTALL_DIR}/${LDPREFIX}/lib
    ${NRN_INSTALL_DIR}/${LDPREFIX}/lib64 
    )

FILE(MAKE_DIRECTORY ${NRN_INSTALL_DIR})
SET(NRN_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nrn)
add_custom_target(nrn  ALL
    DEPENDS ${NRN_INSTALL_DIR}/${LDPREFIX}/bin/nrniv
    )

add_custom_command(OUTPUT ${NRN_INSTALL_DIR}/${LDPREFIX}/bin/nrniv
    COMMAND ./build.sh 
    COMMAND ./configure --with-iv=${IV_INSTALL_DIR} --with-nrnpython --prefix
    ${NRN_INSTALL_DIR} --with-x  --disable-rpath
    COMMAND $(MAKE) 
    COMMAND make install
    WORKING_DIRECTORY ${NRN_SOURCE_DIR}
    VERBATIM
    )

FIND_PACKAGE(PythonLibs REQUIRED)
FIND_PACKAGE(NumPy REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(${NUMPY_INCLUDES})

include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/oc/
    ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/nrnmpi
    )

SET(EXTERNAL_SRC_DIR
    ${CMAKE_CURRENT_SOURCE_DIR}/nrn/share/lib/python/neuron/rxd/geometry3d
    )
add_subdirectory( ${EXTERNAL_SRC_DIR} )

SET(NRNPYTHON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/nrnpython)
add_library(hoc MODULE ${NRNPYTHON_DIR}/inithoc.cpp)

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

add_library(ctng MODULE ${EXTERNAL_SRC_DIR}/ctng.pyx.cpp)
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
    nrnpython
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
    )

add_dependencies(nrn iv)
add_dependencies(hoc nrn)

FIND_PACKAGE(PythonInterp REQUIRED)

# install
install(DIRECTORY ${NRN_INSTALL_DIR}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    )

install(DIRECTORY ${IV_INSTALL_DIR}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    )

#install(CODE
#    "
#    EXECUTE_PROCESS(
#        COMMAND
#        ${PYTHON_EXECUTABLE}${PYTHON_VERSION_MAJOR} setup.py install --prefix ${CMAKE_INSTALL_PREFIX}
#        WORKING_DIRECTORY ${NRN_SOURCE_DIR}/src/nrnpython
#        )"
#    COMPONENT neuron
#    )
#
