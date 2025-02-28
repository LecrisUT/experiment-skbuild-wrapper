cmake_minimum_required(VERSION 3.30)

cmake_file_api(
    QUERY
    API_VERSION 1
    CODEMODEL 2
    CACHE 2
    CMAKEFILES 1
    TOOLCHAINS 1
)

project(main)

set(CMAKE_CXX_STANDARD 17)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

find_package(base CONFIG REQUIRED)

add_executable(main src/main.cpp)
target_link_libraries(main PRIVATE base::base)

install(TARGETS main
    EXPORT mainTargets
)
install(EXPORT mainTargets
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/main
    NAMESPACE main::
)
configure_package_config_file(cmake/mainConfig.cmake.in mainConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/main
)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/mainConfig.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/main
)
