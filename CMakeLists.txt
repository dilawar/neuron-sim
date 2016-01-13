CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
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

SET(NRNPYTHON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nrn/src/nrnpython)
add_custom_target(nrnpython ALL
    DEPENDS ${NRNPYTHON_DIR}/hoc.so
    )
SET(NRNPYTHON_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/_nrnpython)
FILE(MAKE_DIRECTORY ${NRNPYTHON_BUILD_DIR})
add_custom_command(OUTPUT ${NRNPYTHON_DIR}/hoc.so
    COMMAND ${CMAKE_COMMAND} ${NRNPYTHON_DIR}
    COMMAND $(MAKE)
    WORKING_DIRECTORY ${NRNPYTHON_BUILD_DIR}
    )

add_dependencies(nrn iv)
add_dependencies(nrnpython nrn)

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

install(CODE
    "
    EXECUTE_PROCESS(
        COMMAND
        ${PYTHON_EXECUTABLE}${PYTHON_VERSION_MAJOR} setup.py install --prefix ${CMAKE_INSTALL_PREFIX}
        WORKING_DIRECTORY ${NRN_SOURCE_DIR}/src/nrnpython
        )"
    COMPONENT neuron
    )

