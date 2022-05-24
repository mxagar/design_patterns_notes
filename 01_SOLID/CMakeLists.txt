cmake_minimum_required(VERSION 3.0)
project(DP_01_Intro)

set(SRC_DIR .)
set(LIBS '')

include_directories(${SRC_DIR})

set (   SRC_FILES 
        #SRP.cpp 
    )

list(APPEND CMAKE_PREFIX_PATH /opt/homebrew)
find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIR})

# Compilation -> add_executable / add_library
set (CMAKE_CXX_FLAGS "-std=c++14 -O0 -pedantic -Wall -Wfatal-errors -Wextra")
# Linking -> target_link_libraries
set (LDFLAGS "-std=c++14")

# ./srp
add_executable(srp SRP.cpp ${SRC_FILES})
target_link_libraries(srp ${Boost_LIBRARIES})

# ./ocp
add_executable(ocp OCP.cpp ${SRC_FILES})
target_link_libraries(ocp ${Boost_LIBRARIES})

# ./lsp
add_executable(lsp LSP.cpp ${SRC_FILES})
target_link_libraries(lsp ${Boost_LIBRARIES})

# ./isp
add_executable(isp ISP.cpp ${SRC_FILES})
target_link_libraries(isp ${Boost_LIBRARIES})

# ./dip
add_executable(dip DIP.cpp ${SRC_FILES})
target_link_libraries(dip ${Boost_LIBRARIES})