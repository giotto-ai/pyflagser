// #define WITH_HDF5
// #define KEEP_FLAG_COMPLEX_IN_MEMORY
// #define USE_COEFFICIENTS
// #define MANY_VERTICES
#include <iostream>

#include <flagser/src/flagser.cpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(flagser_pybind, m) {
  using persistence_computer_inst =
      persistence_computer_t<directed_flag_complex_compute_t>;
  py::class_<persistence_computer_inst>(m, "persistence_computer_t")
      .def("get_euler_characteristic",
           &persistence_computer_inst::get_euler_characteristic)
      .def("get_betti_numbers",
           py::overload_cast<>(&persistence_computer_inst::get_betti_numbers))
      .def("get_betti_numbers",
           py::overload_cast<size_t>(
               &persistence_computer_inst::get_betti_numbers))
      .def("get_cell_count",
           py::overload_cast<>(&persistence_computer_inst::get_cell_count))
      .def("get_cell_count", py::overload_cast<size_t>(
                                 &persistence_computer_inst::get_cell_count))
      .def("get_persistence_diagram",
           py::overload_cast<>(
               &persistence_computer_inst::get_persistence_diagram))
      .def("get_persistence_diagram",
           py::overload_cast<size_t>(
               &persistence_computer_inst::get_persistence_diagram));

  m.def("compute_homology", [](std::vector<std::string> argv) {
    std::vector<char*> cstrs;
    // Because flagser manage the first argument of argv (binary path) this
    // is a trick to let the user from python call this method without the
    // need to manage this
    argv.insert(argv.begin(), "");
    cstrs.reserve(argv.size());
    for (auto& s : argv) {
      cstrs.push_back(const_cast<char*>(s.c_str()));
    }
    auto arguments = parse_arguments(cstrs.size(), cstrs.data());

    auto positional_arguments = get_positional_arguments(arguments);
    auto named_arguments = get_named_arguments(arguments);
    if (named_arguments.find("help") != named_arguments.end()) {
      print_usage_and_exit(-1);
    }

    if (positional_arguments.size() == 0) {
      print_usage_and_exit(-1);
    }
    const char* input_filename = positional_arguments[0];

    filtered_directed_graph_t graph =
        read_filtered_directed_graph(input_filename, named_arguments);

    size_t max_entries = std::numeric_limits<size_t>::max();
    coefficient_t modulus = 2;
    named_arguments_t::const_iterator it;
    if ((it = named_arguments.find("approximate")) != named_arguments.end()) {
      max_entries = atoi(it->second);
    }
#ifdef USE_COEFFICIENTS
    if ((it = named_arguments.find("modulus")) != named_arguments.end()) {
      modulus = atoi(it->second);
    }
#endif

    return compute_homology(graph, named_arguments, max_entries, modulus);
  });

  m.doc() = "Flagser bindings for python";
}
