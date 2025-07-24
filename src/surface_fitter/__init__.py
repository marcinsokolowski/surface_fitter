from __future__ import print_function
from . import fit_poly_3d
from . import plot_scatter_3d

################################################################################################################################################
# Wrapper function reading a specified text file and calling the main fitting function 
# Chi2 = Sum_k=0^N { (p(x_k,y_k) - D_k ) ^ 2 }            
################################################################################################################################################
def fit_poly( filename , ncols=10, image_size=8192, polynomial_order=7, save_files=True, verbose=0 ) :
   (x_list,y_list,z_list) = fit_poly_3d.read_text_file( filename, ncols=ncols )

   return fit_poly_3d.fit_poly_base( x_list, y_list, z_list, image_size=image_size, polynomial_order=polynomial_order, save_files=save_files, verbose=verbose )
   
def plot_scatter( filename , ncols=10 , plotcol=2, vmin=0, vmax=20 ) : 
   return plot_scatter_3d.plot_scatter( filename, ncols=ncols, plotcol=plotcol, vmin=vmin, vmax=vmax )


def hi(name: str):
   print(f"Hi there, {name}")
   
print(f"{__file__} imported")
   