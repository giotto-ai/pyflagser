from ._version import __version__

from .flagio import loadflag, saveflag
from .flagser import flagser_static, flagser_persistence

__all__ = ['loadflag', 'saveflag', 'flagser_static', 'flagser_persistence',
           '__version__']
