from ._version import __version__

from .flagio import load_static_flag, load_persistence_flag, \
    save_static_flag, save_persistence_flag
from .flagser import flagser_static, flagser_persistence

__all__ = ['load_static_flag', 'load_persistence_flag',
           'save_static_flag', 'save_persistence_flag',
           'flagser_static', 'flagser_persistence',
           '__version__']
