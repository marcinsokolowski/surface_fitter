from __future__ import print_function
# from . import fit_poly_3d
# from . import plot_scatter_3d
from .fit_poly_3d import fit_poly
from .plot_scatter_3d import plot_scatter
from .surface_generator import generate_data

def hi(name: str):
   print(f"Hi there, {name}")
   
print(f"{__file__} imported")
   