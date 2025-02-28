find_package(Python 3.10 REQUIRED COMPONENTS Development.Module)
find_package(pybind11 CONFIG REQUIRED)

# For some reason order matters here
python_add_library(_run_mod MODULE _run_mod.cpp WITH_SOABI)
target_link_libraries(_run_mod PRIVATE pybind11::headers base::base)

if(SKBUILD)
    scikit_build_add_rpath(_run_mod base::base ".")
    install(TARGETS _run_mod DESTINATION ".")
endif()
