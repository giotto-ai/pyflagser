#include <stdio.h>
#include <iostream>

#include <flagser/src/flagser-count.cpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(flagser_count_pybind, m) {
  m.doc() = "Python interface for flagser_count";

  m.def("compute_cell_count", [](std::vector<value_t>& vertices,
                                 std::vector<std::vector<value_t>>& edges,
                                 bool directed) {
    // Save std::cout status
    auto cout_buff = std::cout.rdbuf();

    // flagser-count's parameters
    flagser_parameters params;

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

    // Running flagser-count's count_cells routine
    auto cell_count = count_cells(graph, params);

    // Re-enable again cout
    std::cout.rdbuf(cout_buff);

    return cell_count;
  });
}
