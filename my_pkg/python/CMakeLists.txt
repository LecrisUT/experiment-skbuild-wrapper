cmake_minimum_required(VERSION 3.30)

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
function(scikit_build_add_rpath requesting_target imported_target)
    # Save the rpath origin symbol
    if(APPLE)
        set(origin_symbol "@rpath")
    else()
        set(origin_symbol "$ORIGIN")
    endif()
    # Check if the imported_target is imported
    get_target_property(imported ${imported_target} IMPORTED)
    if(NOT imported)
        # TODO: What to do with non-imported targets?
        return()
    endif()
    # Check what type of imported_target it is
    get_target_property(type ${imported_target} TYPE)
    if(NOT type STREQUAL "SHARED_LIBRARY")
        # We only add rpaths to shared library
        # Technically EXECUTABLE could also be linked against
        # TODO: Are there rpaths in static library and do they propagate
        # TODO: Is there some handling to do for `INTERFACE_LIBRARY`/`OBJECT_LIBRARY`?
        return()
    endif()
    # Get the library file location
    get_target_property(location ${imported_target} LOCATION)
    # Take the parent directory
    cmake_path(GET location PARENT_PATH location)
    # Get the relative path w.r.t.
    cmake_path(RELATIVE_PATH location
        # scikit-build-core: provide `mocked_wheel_install_dir` pointing to the
        # `wheel.install-dir` in the build environment
        BASE_DIRECTORY ${mocked_wheel_install_dir}
    )
    # Invert the path from CMAKE_INSTALL_LIBDIR to `wheel.install-dir`
    set(path_to_wheel_install_dir ".")
    cmake_path(RELATIVE_PATH path_to_wheel_install_dir
        BASE_DIRECTORY ${CMAKE_INSTALL_LIBDIR}
    )
    # Construct the rpath needed by the
    cmake_path(APPEND rpath
        "${path_to_wheel_install_dir}"
        "${location}"
    )
    cmake_path(NORMAL_PATH rpath)
    # We add `origin_symbol` at the end to not interfere with cmake_path
    set(rpath "${origin_symbol}/${rpath}")
    set_property(TARGET ${requesting_target} APPEND
        PROPERTY INSTALL_RPATH "${rpath}"
    )
endfunction()

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
    scikit_build_add_rpath(main base::base)
    scikit_build_add_wrapper(main)
endif()
