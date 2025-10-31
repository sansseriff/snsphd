# Change Log

## [0.2.0] - 2025-10-31

- Removed numba dependency.
- Made heavy dependencies optional and available via extras:
  - SciPy (hist utilities): install with `pip install "snsphd[scipy]"`
  - Bokeh + IPython (viz utilities): install with `pip install "snsphd[viz]"`
  - Everything: `pip install "snsphd[all]"`
- Updated `__init__.py` to import optional submodules lazily so `import snsphd` works without the extras installed.

## [0.1.4] - 2024-10-17

- Updated to numpy 2.0 and number 0.60.0
