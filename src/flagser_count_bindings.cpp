// #define WITH_HDF5
// #define KEEP_FLAG_COMPLEX_IN_MEMORY
// #define USE_COEFFICIENTS
// #define MANY_VERTICES
#include <stdio.h>
#include <iostream>

#include <flagser/include/argparser.h>
#include <flagser/src/flagser-count.cpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(flagser_count_pybind, m) {
  m.def("compute_cell_count", [](std::vector<value_t>& vertices,
                                 std::vector<std::vector<value_t>>& edges,
                                 bool directed) {
    // Save std::cout status
    auto cout_buff = std::cout.rdbuf();
    named_arguments_t named_arguments;

    HAS_EDGE_FILTRATION has_edge_filtration =
        HAS_EDGE_FILTRATION::TOO_EARLY_TO_DECIDE;

    named_arguments["out"] = "output_flagser_file";
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

    auto ret = count_cells(graph, named_arguments);

    if (remove(named_arguments["out"]) != 0)
      perror("Error deleting flagser output file");

    // re enable again cout
    std::cout.rdbuf(cout_buff);

    return ret;
  });

  m.doc() = "Python bindings for flagser_count";
}
