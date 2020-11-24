#include <iostream>
#include <string>
#include <stdio.h>

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
           py::overload_cast<size_t>(&PersistenceComputer::get_betti_numbers))
      .def("get_cell_count",
           py::overload_cast<>(&PersistenceComputer::get_cell_count))
      .def("get_cell_count",
           py::overload_cast<size_t>(&PersistenceComputer::get_cell_count))
      .def("get_persistence_diagram",
           py::overload_cast<>(&PersistenceComputer::get_persistence_diagram))
      .def("get_persistence_diagram",
           py::overload_cast<size_t>(
               &PersistenceComputer::get_persistence_diagram));

  m.def("compute_homology", [](std::vector<value_t>& vertices,
                               std::vector<std::vector<value_t>>& edges,
                               unsigned short min_dim, short max_dim,
                               bool directed, coefficient_t modulus,
                               signed int approximation,
                               std::string filtration) {
    flagser_parameters params;

    // Save std::cout status
    auto cout_buff = std::cout.rdbuf();

    // Minimum dimension parameter
    params.min_dimension = min_dim;

    // Maximum dimension parameter
    unsigned short effective_max_dim = max_dim;
    if (max_dim < 0) {
      effective_max_dim = std::numeric_limits<unsigned short>::max();
    }
    params.max_dimension = effective_max_dim;

    // Filtration argument
    params.filtration_algorithm.reset(get_filtration_computer(filtration));

    // Modulus/Coefficient parameter
    params.modulus = modulus;

    // If approximation is negative it falls back to type::numeric_limits
    params.approximate_computation = approximation ? true : false;
    params.max_entries =
        params.approximate_computation > 0 ? approximation : params.max_entries;

    // Directed parameter
    params.directed = directed;

    // Output file is not used but set to an temporary file
    // See: https://en.cppreference.com/w/cpp/io/c/tmpnam
    params.output_name = std::string(std::tmpnam(nullptr));

    // Remove output file if already present
    remove(params.output_name.c_str());

    // Building the filtered directed graph
    auto graph = filtered_directed_graph_t(vertices, params.directed);

    HAS_EDGE_FILTRATION has_edge_filtration =
        HAS_EDGE_FILTRATION::TOO_EARLY_TO_DECIDE;

    // If we have at least one edge
    if (edges.size() && has_edge_filtration == HAS_EDGE_FILTRATION::MAYBE) {
      // If the edge has three components, the last is the filtration
      // value
      has_edge_filtration = edges[0].size() == 2 ? HAS_EDGE_FILTRATION::NO
                                                 : HAS_EDGE_FILTRATION::YES;
    }

    for (auto& edge : edges) {
      if (has_edge_filtration == NO) {
        graph.add_edge(edge[0], edge[1]);
      } else {
        if (edge[2] < std::max(vertices[edge[0]], vertices[edge[1]])) {
          std::string err_msg =
              "The data contains an edge "
              "filtration that contradicts the vertex "
              "filtration, the edge (" +
              std::to_string(edge[0]) + ", " + std::to_string(edge[1]) +
              ") has filtration value " + std::to_string(edge[2]) +
              ", which is lower than min(" + std::to_string(vertices[edge[0]]) +
              ", " + std::to_string(vertices[edge[1]]) +
              "), the filtrations of its edges.";
          throw std::runtime_error(err_msg);
        }
        graph.add_filtered_edge((vertex_index_t)edge[0],
                                (vertex_index_t)edge[1], edge[2]);
      }
    }

    // Disable cout
    std::cout.rdbuf(nullptr);

    // Running flagser's compute_homology routine
    auto subgraph_persistence_computer = compute_homology(graph, params);

    // Re-enable again cout
    std::cout.rdbuf(cout_buff);

    // Remove generated output file
    if (remove(params.output_name.c_str()) != 0) {
      throw std::runtime_error("Error deleting flagser output file");
    }

    return subgraph_persistence_computer;
  });
}
