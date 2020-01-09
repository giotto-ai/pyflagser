from ._version import __version__

from .flagio import loadflag, saveflag
from .flagser import flagser

__all__ = ['loadflag', 'saveflag', 'flagser', '__version__']
