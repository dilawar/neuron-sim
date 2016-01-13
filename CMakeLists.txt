CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(neuron)


INCLUDE_DIRECTORIES(
    ${CMAKE_CURRENT_SOURCE_DIR}/nrn
    ${CMAKE_CURRENT_SOURCE_DIR}/iv
)

SET(IV_INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/_iv)
FILE(MAKE_DIRECTORY ${IV_INSTALL_DIR})
SET(IV_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/iv)

add_custom_target(iv  ALL
    DEPENDS ${IV_SOURCE_DIR}/include/ivversion.h
    )

add_custom_command(OUTPUT ${IV_SOURCE_DIR}/include/ivversion.h
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
    DEPENDS ${NRN_INSTALL_DIR}/x86_64/bin/nrngui
    )

SET(ENV{LDFLAGS} "-L ${NRN_INSTALL_DIR}/x86_64/lib64")
add_custom_command(OUTPUT ${NRN_INSTALL_DIR}/x86_64/bin/nrngui
    COMMAND ./build.sh
    COMMAND ./configure --with-iv=${IV_INSTALL_DIR} --prefix ${NRN_INSTALL_DIR} --with-nrnpython 
    COMMAND $(MAKE) 
    COMMAND make install
    WORKING_DIRECTORY ${NRN_SOURCE_DIR}
    VERBATIM
    )

add_dependencies(nrn iv)

# install
install(DIRECTORY ${NRN_INSTALL_DIR}/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    )

