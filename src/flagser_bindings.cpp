#include <stdio.h>
#include <iostream>

#include <flagser/include/argparser.h>
#include <flagser/src/flagser.cpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;


#ifdef USE_COEFFICIENTS
PYBIND11_MODULE(flagser_coeff_pybind, m) {
#else
PYBIND11_MODULE(flagser_pybind, m) {
#endif

  m.doc() = "Python interface for flagser";

  m.attr("AVAILABLE_FILTRATIONS") = custom_filtration_computer;

  using PersistenceComputer =
    persistence_computer_t<directed_flag_complex_compute_t>;

  py::class_<PersistenceComputer>(m, "PersistenceComputer", py::module_local())
      .def("get_euler_characteristic",
           &PersistenceComputer::get_euler_characteristic)
      .def("get_betti_numbers",
           py::overload_cast<>(&PersistenceComputer::get_betti_numbers))
      .def("get_betti_numbers",
           py::overload_cast<size_t>(
               &PersistenceComputer::get_betti_numbers))
      .def("get_cell_count",
           py::overload_cast<>(&PersistenceComputer::get_cell_count))
      .def("get_cell_count", py::overload_cast<size_t>(
                                 &PersistenceComputer::get_cell_count))
      .def("get_persistence_diagram",
           py::overload_cast<>(
               &PersistenceComputer::get_persistence_diagram))
      .def("get_persistence_diagram",
           py::overload_cast<size_t>(
               &PersistenceComputer::get_persistence_diagram));

  m.def("compute_homology", [](std::vector<value_t>& vertices,
                               std::vector<std::vector<value_t>>& edges,
                               unsigned short min_dim, short max_dim,
                               bool directed, coefficient_t modulus,
                               signed int approximation,
                               std::string filtration) {
    // Save std::cout status
    auto cout_buff = std::cout.rdbuf();

    // flagser's routine needs to be passed command line arguments
    named_arguments_t named_arguments;

    // Passing minimum dimension as a command line argument
    std::string str_min = std::to_string(min_dim);
    named_arguments["min-dim"] = str_min.c_str();

    // Passing maximum dimension as a command line argument
    unsigned short effective_max_dim = max_dim;
    if (max_dim < 0) {
      effective_max_dim = std::numeric_limits<unsigned short>::max();
    }
    std::string str_max = std::to_string(effective_max_dim);
    named_arguments["max-dim"] = str_max.c_str();

    // Passing filtration as a command line argument
    named_arguments["filtration"] = filtration.c_str();

    // Output file is not used but set to an arbitrary file
    named_arguments["out"] = "output_flagser_file";

    // Remove output file if already present
    remove(named_arguments["out"]);

    // Building the filtered directed graph
    auto graph = filtered_directed_graph_t(vertices, directed);

    HAS_EDGE_FILTRATION has_edge_filtration =
      HAS_EDGE_FILTRATION::TOO_EARLY_TO_DECIDE;

    // If we have at least one edge
    if (edges.size() && has_edge_filtration == HAS_EDGE_FILTRATION::MAYBE) {
      // If the edge has three components, the last is the filtration value
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

    // If approximation is negative it falls back to type::numeric_limits
    size_t max_entries =
        approximation >= 0 ? approximation : std::numeric_limits<size_t>::max();

    // Disable cout
    std::cout.rdbuf(nullptr);

    // Running flagser's compute_homology routine
    auto output = compute_homology(graph, named_arguments, max_entries, modulus);

    // Re-enable again cout
    std::cout.rdbuf(cout_buff);

    // Remove generate output file
    if (remove(named_arguments["out"]) != 0)
      perror("Error deleting flagser output file");

    return output;
  });
}
