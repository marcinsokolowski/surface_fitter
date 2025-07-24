from __future__ import print_function
########################################################################################################################
#
# Developed by Marcin Sokolowski (marcin.sokolowski@curtin.edu.au) , version 1.00 , 2021-11
# Plots 3 column file and creates a 3D plot 
########################################################################################################################
import numpy as np
import os
import sys
from mpl_toolkits.mplot3d import Axes3D
import copy
from optparse import OptionParser,OptionGroup

import re

import matplotlib as m
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid') # in python2 was : seaborn-whitegrid')

def parse_options():
   usage="Usage: %prog [options]\n"
   usage+='\tPlot 3 column file with values X Y Z\n'
   parser = OptionParser(usage=usage,version=1.00)
   parser.add_option('--vmin','--min_z','--min_value',dest="vmin",default=0.00, help="Vmin value for colorbar [default %]",type="float")
   parser.add_option('--vmax','--max_z','--max_value',dest="vmax",default=20.00, help="Vmax value for colorbar [default %]",type="float")
   parser.add_option('--ncols','--n_columns','--num_columns',dest="ncols",default=10, help="Number of columns in a file [default %]",type="int")
   parser.add_option('--plotcol','--plot_column','--plot_col',dest="plotcol",default=2, help="Plot column when ncols != 10 [default %]",type="int")
   
#   parser.add_option('--image_size','--size',dest="image_size",default=8192, help="Image size [default %]",type="int")

   (options, args) = parser.parse_args()

   return (options, args)




#  X   Y   RA_image[deg]    DEC_image[deg]  Flux_image[Jy]   RA_gleam[deg]    DEC_gleam[deg]    Flux_gleam[Jy]   AngDist[arcsec]    CalConst
# 16   2930   284.3990    -23.1885    0.023    284.3999    -23.1880    0.569    3.40    24.60445805 
def read_text_file( filename , ncols=10 , plotcol=2 , min_val=-1e20, max_val=1e20, verbose=0 ) :
   x_list = []
   y_list = []
   calconst_list = []

   if os.path.exists(filename) and os.stat(filename).st_size > 0 :
      file=open(filename,'r')
      data=file.readlines()
      for line in data :
         if line[0] != "#" :
#            words = line.split(' ')
            words = re.split( '\s+' , line )

            if verbose > 0 :         
               print("DEBUG : line = %s -> |%s|%s|" % (line,words[0+0],words[1+0]))
            x = float(words[0+0])
            y = float(words[1+0])
            calconst = float(words[plotcol+0])
         
            if calconst > min_val and calconst < max_val :
               x_list.append(x)
               y_list.append(y)
               calconst_list.append(calconst)               
            
      file.close()      
   else :
      print("WARNING : empty or non-existing file %s" % (filename))

   print("READ %d values from file %s" % (len(x_list),filename))
   
   return (x_list,y_list,calconst_list)

def plot_scatter( filename , ncols=5, plotcol=2, vmin=0, vmax=20, verbose=0 ) :   
   (x_list,y_list,calconst_list) = read_text_file( filename , ncols=ncols, plotcol=plotcol, min_val=vmin, max_val=vmax, verbose=verbose )
   # rng = np.random.RandomState(0)
   x = x_list # rng.randn(100)
   y = y_list # rng.randn(100)
   colors = calconst_list
   sizes = 50 # * rng.rand(100)

   # https://stackoverflow.com/questions/3373256/set-colorbar-range-in-matplotlib
   cdict = {
     'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
     'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
     'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
   }

   cm = m.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
   plt.clf()
   plt.xlabel('X pixel')
   plt.ylabel('Y pixel')
   
   # 3D : https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
   ax = plt.axes(projection='3d')
   ax.scatter3D( x, y, colors, c=colors, cmap='rainbow' , vmin=vmin, vmax=vmax );
   
#   plt.colorbar();  # show color scale   
   plt.show()
   

if __name__ == '__main__':
   filename = "mean_stokes_I_2axis_gleamcal.txt"
   if len(sys.argv) > 1:
      filename = sys.argv[1]
      
   (options, args) = parse_options()   
      
   plot_scatter( filename , ncols = options.ncols, plotcol=options.plotcol , vmin=options.vmin, vmax=options.vmax )   
      
      


