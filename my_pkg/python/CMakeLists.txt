cmake_minimum_required(VERSION 3.30)

cmake_file_api(
    QUERY
    API_VERSION 1
    CODEMODEL 2
    CACHE 2
    CMAKEFILES 1
    TOOLCHAINS 1
)

project(main_python)

set(CMAKE_CXX_STANDARD 17)

include(GNUInstallDirs)

# Currently the dependencies need to be handled here
# otherwise the target is not visible
# TODO: How to relax this requirement?
find_package(base CONFIG REQUIRED)

find_package(main CONFIG)
if(NOT main_FOUND)
    add_subdirectory(.. _deps/main-build)
endif()

# Ideally `scikit-build-core` can provide a wrapper for this since
# It can find out if a dependency is in a build isolation or not
# It can check if a package is from site-packages or the system

function(scikit_build_add_wrapper target)
    file(READ _run_wrapper.py.in wrapper_template)
    string(CONFIGURE "${wrapper_template}" wrapper_template @ONLY)
    file(GENERATE OUTPUT _run_${target}.py
        CONTENT "${wrapper_template}"
    )
    install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/_run_${target}.py
        DESTINATION .
    )
endfunction()

if(SKBUILD)
    cmake_path(SET mocked_wheel_install_dir NORMALIZE
        "${base_PREFIX}/../my_pkg"
    )
    scikit_build_add_wrapper(main)
    install(IMPORTED_RUNTIME_ARTIFACTS main)
#    install(TARGETS main
#        RUNTIME DESTINATION ${SKBUILD_SCRIPTS_DIR}
#    )
endif()

add_subdirectory(bindings)
