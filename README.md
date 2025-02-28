# scikit-build-core wrapper experiment

Experimenting what helper functions and wrappers could be provided by `scikit-build-core` to
simplify user setups.

- `base` is a simple compiled dependency that could be provided on PyPI
- `my_pkg` is the main project we want to build


## Goal

- Both `base` and `my_pkg` should be buildable according to distro guidelines
- Both `base` and `my_pkg` should be buildable via `pip install` and be packagable for PyPI
- Building python wrappers manually is not supported


## Status
- [x] Support Linux and MacOS system
  - `RPATH` is patched to make it 
- [ ] Support Windows
- [ ] Support distro installation
