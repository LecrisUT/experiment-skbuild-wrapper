#include <pybind11/pybind11.h>
#include <base.h>

void run_main() {
    base::hello();
}

namespace py = pybind11;

PYBIND11_MODULE(_run_mod, m) {
    m.def("run_main", &run_main);
}