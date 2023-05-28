# PH-Baseliner:
Tools to automatically setup the code-minimum 'Baseline' values for Passive House models.

## Usage:
The most basic usage is a to edit the values of an existing PHPP file to match 
a desired code-minimum configuration.
```python
>>> # --- Connect to an instance of Excel with your PHPP file open.
>>> import xlwings as xw
>>> from PHX.xl import xl_app
>>> from PHX.PHPP import phpp_app
>>> xl = xl_app.XLConnection(xl_framework=xw)
>>> _phpp_conn = phpp_app.PHPPConnection(xl)
>>> 
>>> # --- Load the Code baseline model you would like to follow.
>>> import pathlib
>>> from ph_baseliner.codes.model import BaselineCode
>>> baseline_code_file_path = pathlib.Path(".", "ph_baseliner", "codes", "2020_ECCCNY.json")
>>> _baseline_code = BaselineCode.parse_file(baseline_code_file_path)
>>> 
>>> # --- Set the PHPP values as desired in the various Worksheets
>>> from ph_baseliner.codes.options import ClimateZones
>>> from ph_baseliner.phpp.areas import set_baseline_envelope_constructions
>>> set_baseline_envelope_constructions(_phpp_conn, _baseline_code, ClimateZones.CZ4)
```

- - -
Note: The baseliner will change the values of the PHPP file, and so you should 
be sure to make a backup copy before using this tool.

- - - 
![Tests](https://github.com/PH-Tools/PHX/actions/workflows/ci.yaml/badge.svg )
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)
[![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)