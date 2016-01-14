cmake_minimum_required(VERSION 2.6)
FILE(GLOB CYTHON_SRC "*.pyx")
FIND_PACKAGE(Cython REQUIRED)
foreach( CYFILE ${CYTHON_SRC})
    MESSAGE(STATUS "Generating ${CYFILE}.cpp from ${CYFILE}")
    execute_process(
        COMMAND ${CYTHON_EXECUTABLE} ${CYFILE} -o ${CYFILE}.cpp
        )
endforeach()
