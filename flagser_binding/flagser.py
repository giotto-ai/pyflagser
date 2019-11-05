#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: flagser.py
Description: This file implements the python of the flagser library written in
    C++.
"""
__license__ = "Apache 2.0"
__credits__ = ["Daniel Lütgehetmann"]


import os
from flagser_pybind import compute_homology


def flagser_file(file_data):
    """Compute persistent homology for directed flag complexes. Important: the
    input graphs cannot contain self-loops. i.e. edges that start and end in
    the same vertex.

    Parameters
    ----------
    file_data: the path of the data file containing directed flags.

    Returns
    -------
    A  list of dictionary holding all of the results of the computation by
    graphs
    {
     'dgms': list (size maxdim) of ndarray (n_pairs, 2)
        A list of persistence diagrams, one for each dimension less
        than maxdim. Each diagram is an ndarray of size (n_pairs, 2)
        with the first column representing the birth time and the
        second column representing the death time of each pair.
     'cell_count': list (int)
        Cell count per dimension
     'betti': ndarray(int)
        Betti number computed by dimension
     'euler': int
        Euler characteristic
    }
    """
    output_file = 'output_flagser_file'

    # Clean if the file from a precedent run was not deleted
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Due to current implementation of flagser, an output file is required.
    # Because of that, an temporary output file is provided and will be delete
    # after the completion of `compute_homology
    args = ['--out', output_file, file_data]

    homology = compute_homology(args)

    # Clean the file genereated by flagser library
    os.remove(output_file)

    # Creating dictionary of returns values
    graphs = []
    for dim in homology:
        ret_dict = {}
        ret_dict.update({'dgms': dim.get_persistence_diagram()})
        ret_dict.update({'cell_count': dim.get_cell_count()})
        ret_dict.update({'betti': dim.get_betti_numbers()})
        ret_dict.update({'euler': dim.get_euler_characteristic()})
        graphs.append(ret_dict)

    return graphs


def flagser(vertices, edges, directed=True):
    """Compute persistent homology for directed flag complexes. Important: the
    input graphs cannot contain self-loops. i.e. edges that start and end in
    the same vertex.

    Parameters
    ----------
    vertices: TODO
    edges: TODO
    directed: if true, computes the directed flag complex. Otherwise it
    computes the undirected flag

    Returns
    -------
    A  list of dictionary holding all of the results of the computation by
    graphs
    {
     'dgms': list (size maxdim) of ndarray (n_pairs, 2)
        A list of persistence diagrams, one for each dimension less
        than maxdim. Each diagram is an ndarray of size (n_pairs, 2)
        with the first column representing the birth time and the
        second column representing the death time of each pair.
     'cell_count': list (int)
        Cell count per dimension
     'betti': ndarray(int)
        Betti number computed by dimension
     'euler': int
        Euler characteristic
    }
    """
    output_file = 'output_flagser_file'

    # Clean if the file from a precedent run was not deleted
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Due to current implementation of flagser, an output file is required.
    # Because of that, an temporary output file is provided and will be delete
    # after the completion of `compute_homology

    homology = compute_homology(vertices, edges, directed)

    # Clean the file genereated by flagser library
    os.remove(output_file)

    # Creating dictionary of returns values
    graphs = []
    for dim in homology:
        ret_dict = {}
        ret_dict.update({'dgms': dim.get_persistence_diagram()})
        ret_dict.update({'cell_count': dim.get_cell_count()})
        ret_dict.update({'betti': dim.get_betti_numbers()})
        ret_dict.update({'euler': dim.get_euler_characteristic()})
        graphs.append(ret_dict)

    return graphs


if __name__ == "__main__":
    pass
