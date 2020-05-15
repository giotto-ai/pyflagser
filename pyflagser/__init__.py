from ._version import __version__

from .flagio import load_unweighted_flag, load_weighted_flag, \
    save_unweighted_flag, save_weighted_flag
from .flagser import flagser_unweighted, flagser_weighted

__all__ = ['load_unweighted_flag', 'load_weighted_flag',
           'save_unweighted_flag', 'save_weighted_flag',
           'flagser_unweighted', 'flagser_weighted',
           '__version__']
