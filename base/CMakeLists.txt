cmake_minimum_required(VERSION 3.30)

cmake_file_api(
    QUERY
    API_VERSION 1
    CODEMODEL 2
    CACHE 2
    CMAKEFILES 1
    TOOLCHAINS 1
)

project(base)

set(CMAKE_CXX_STANDARD 17)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

add_library(base SHARED)
add_subdirectory(src)

install(TARGETS base
    EXPORT baseTargets
    FILE_SET base_headers
)
install(EXPORT baseTargets
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/base
    NAMESPACE base::
)
set(base_PREFIX ".")
configure_package_config_file(cmake/baseConfig.cmake.in baseConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/base
    PATH_VARS base_PREFIX
)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/baseConfig.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/base
)

if(SKBUILD)
    install(TARGETS base
        RUNTIME DESTINATION ${SKBUILD_SCRIPTS_DIR}
    )
endif()
