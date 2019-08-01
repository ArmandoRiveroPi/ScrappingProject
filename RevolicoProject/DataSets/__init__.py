"""This module should care of providing data sets access for modeling, inference, etc.

From several data sources it provides access to several sets:
    Toy dataset: tiny set used to test the plumbing of code, really useless otherwise
    Exploration dataset: midsize set used to try several models and keeping the most promising
    Train dataset: full set for fine tuning the very best models, do hyperparameter search and etc. (superset of the previous)
    Test dataset: reserved only for the latest testing of the model (separated from the previous)

The access to the data probably is going to be reading-only
"""
from .data_set_provider_class import DataSetProvider
