// #define WITH_HDF5
// #define KEEP_FLAG_COMPLEX_IN_MEMORY
// #define USE_COEFFICIENTS
// #define MANY_VERTICES
#include <stdio.h>
#include <iostream>

#include <flagser/include/argparser.h>
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

  m.def("compute_homology", [](std::vector<value_t>& vertices,
                               std::vector<std::vector<value_t>>& edges,
                               unsigned short min_dim, short max_dim,
                               bool directed, coefficient_t modulus,
                               signed int approximation,
                               std::string filtration) {
    // Save std::cout status
    auto cout_buff = std::cout.rdbuf();

    HAS_EDGE_FILTRATION has_edge_filtration =
        HAS_EDGE_FILTRATION::TOO_EARLY_TO_DECIDE;

    // Approximation should only be a positive value
    // Otherwise it falls back to type::numeric_limits
    size_t max_entries =
        approximation >= 0 ? approximation : std::numeric_limits<size_t>::max();

    unsigned short effective_max_dim = max_dim;
    std::string default_filtration = "max";

    if (max_dim < 0)
      effective_max_dim = std::numeric_limits<unsigned short>::max();

    named_arguments_t named_arguments;
    named_arguments["out"] = "output_flagser_file";
    named_arguments["--max-dim"] = std::to_string(effective_max_dim).c_str();
    named_arguments["--min-dim"] = std::to_string(min_dim).c_str();

    // Is filtration supported ?
    if (std::find(custom_filtration_computer.begin(),
                  custom_filtration_computer.end(),
                  filtration) == custom_filtration_computer.end()) {
      std::cout << filtration << " not found, fallback to "
                << default_filtration << "\n";
      filtration = default_filtration;

      std::cout << "Implemented filtrations:\n";
      for (auto& elem : custom_filtration_computer) {
        if (elem != custom_filtration_computer.back())
          std::cout << elem << ", ";
        else
          std::cout << elem << "\n";
      }
    }

    named_arguments["--filtration"] = filtration.c_str();

    remove(named_arguments["out"]);

    auto graph = filtered_directed_graph_t(vertices, directed);

    // If we have at least one vertice
    if (edges.size() && has_edge_filtration == HAS_EDGE_FILTRATION::MAYBE) {
      // If the edge has three components, then there are also
      // filtration values, which we assume to come last
      has_edge_filtration = edges[0].size() == 2 ? HAS_EDGE_FILTRATION::NO
                                                 : HAS_EDGE_FILTRATION::YES;
    }

    for (auto& edge : edges) {
      if (has_edge_filtration == NO) {
        graph.add_edge(edge[0], edge[1]);
      } else {
        if (edge[2] < std::max(vertices[edge[0]], vertices[edge[1]])) {
          std::cerr << "The data contains an edge "
                       "filtration that contradicts the vertex "
                       "filtration, the edge ("
                    << edge[0] << ", " << edge[1] << ") has filtration value "
                    << edge[2] << ", which is lower than min("
                    << vertices[edge[0]] << ", " << vertices[edge[1]]
                    << "), the filtrations of its edges.";
          exit(-1);
        }
        graph.add_filtered_edge((vertex_index_t)edge[0],
                                (vertex_index_t)edge[1], edge[2]);
      }
    }

    std::cout.rdbuf(nullptr);

    auto ret = compute_homology(graph, named_arguments, max_entries, modulus);

    if (remove(named_arguments["out"]) != 0)
      perror("Error deleting flagser output file");

    // re enable again cout
    std::cout.rdbuf(cout_buff);

    return ret;
  });

  m.attr("implemented_filtrations") = custom_filtration_computer;

  m.doc() = "Python bindings for flagser";
}
