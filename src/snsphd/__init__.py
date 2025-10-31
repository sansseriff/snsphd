# -*- coding: utf-8 -*-

"""Top level package for snsphd.

Default install keeps heavy, optional dependencies out. Submodules that require
optional extras are imported lazily/optionally to avoid import-time failures.
"""

from . import obj  # noqa: F401
from . import help  # noqa: F401
from . import layout  # noqa: F401

# Optional submodules: only available if extras are installed
try:  # viz depends on bokeh and ipython (extra: "viz")
    from . import viz  # type: ignore
except Exception:  # pragma: no cover - optional dependency not installed
    viz = None  # noqa: F401

try:  # hist depends on scipy (extra: "scipy")
    from . import hist  # type: ignore
except Exception:  # pragma: no cover - optional dependency not installed
    hist = None  # noqa: F401

# from . import clock


__author__ = """Andrew Mueller"""
__email__ = """andrewstermueller@gmail.com"""
__version__ = "0.2.5"

__all__ = [
    "obj",
    "help",
    "layout",
    "viz",
    "hist",
]
