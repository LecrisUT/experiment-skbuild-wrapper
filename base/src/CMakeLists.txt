target_sources(base
    PRIVATE
        base.cpp
    PUBLIC FILE_SET base_headers TYPE HEADERS
    FILES
        base.h
)
target_include_directories(base
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
