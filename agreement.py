#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Calculate various agreement measures.
# Copyright (C) 2012 Marcin Włodarczak
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

import itertools
import numpy as np

# --------------
# Fleiss's kappa
# --------------

def fleiss_observed_agreement(a):
    """Return the observed agreement for the input array."""

    def per_subject_agreement(row):
        """Return the observed agreement for the i-th subject."""
        number_of_objects = np.sum(row)
        return (np.sum(np.square(row)) - number_of_objects) / (number_of_objects * (number_of_objects - 1))

    row_probabilities = np.apply_along_axis(per_subject_agreement, axis=1, arr=a)
    return np.mean(row_probabilities)

def fleiss_chance_agreement(a):
    """Returns the chance agreement for the input array."""

    def per_category_probabilities(a):
        """The proportion of all assignments which were to the j-th category."""
        cat_sums = np.sum(a, axis=0)
        return cat_sums / np.sum(cat_sums)

    return np.sum(np.square(per_category_probabilities(a)))

def fleiss_kappa(a):
    """Calculates Fleiss's kappa for the input array (with categories
    in columns and items in rows)."""
    p = observed_agreement(a)
    p_e = chance_agreement(a)
    return (p - p_e) / (1 - p_e)

# -------------
# Cohen's kappa
# -------------

def cohen_kappa(a):
    """Calculates Cohen's kappa for the input array."""
    totsum = np.sum(a)
    colsums = np.sum(a, 0)
    rowsums = np.sum(a, 1)
    # Observed agreement.
    p = np.sum(np.diagonal(a)) / totsum
    # Chance agreement.
    p_e = np.sum((colsums * rowsums) / totsum**2)
    return (p - p_e) / (1 - p_e)

# ----------
# Scott's pi
# ----------

def scott_pi(a):
    """Calculates Scott's Pi for the input array."""
    totsum = np.sum(a)
    colsums = np.sum(a, 0)
    rowsums = np.sum(a, 1)
    # Observed agreement.
    p = np.sum(np.diagonal(a)) / totsum
    # Chance agreement.
    joint_marginal_props = (colsums + rowsums) / (2 * totsum)
    p_e = np.sum(joint_marginal_props**2)
    return (p - p_e) / (1 - p_e)

# ----------------------------------------------------------
# Fuctions producing contingency tables from lists of labels
# ----------------------------------------------------------


def two_raters_table(l):
    """Returns a contingency table for two raters given a list of
    zipped labels."""
    sublists_lengths = [len(x) for x in l]
    if any([x != 2 for x in sublists_lengths]):
        Exception('The length of sublists must be equal to 2')
    if sublists_lengths.count(sublists_lengths[0]) != len(sublists_lengths):
        Exception('The lengths of sublists differ.')
    # List of unique labels from both lists.
    categories = list(set(itertools.chain(*l)))
    # Dictionary translating labels into consecutive integers.
    trans = dict([(categories[x], x) for x in range(len(categories))])
    cont_table = np.zeros([len(categories), len(categories)])
    for labels in l:
        cont_table[trans[labels[0]], trans[labels[1]]] += 1
    return cont_table

def n_raters_table(l):
    """Returns a contingency table for n >= 2 raters (with categories
    in columns and items in rows) given a list of zipped labels."""
    sublists_lengths = [len(x) for x in l]
    if any([x < 2 for x in sublists_lengths]):
        Exception('The length of sublists must be at least 2')
    if sublists_lengths.count(sublists_lengths[0]) != len(sublists_lengths):
        Exception('The lengths of sublists differ')
    # List of unique labels from all lists.
    categories = list(set(itertools.chain(*l)))
    cont_table = np.array([x.count(y) for x in l for y in categories])
    cont_table.shape = (sublists_lengths[0], len(categories))
    return cont_table
