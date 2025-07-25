from __future__ import print_function
########################################################################################################################
#
# Developed by Marcin Sokolowski (marcin.sokolowski@curtin.edu.au) , version 1.00 , 2021-11
# Fits a surface represented by a polynomial of an arbitrary order by calculating derivative over each cofficient, equaling them to zero and forming as many equations as many parameters
#
#  Test :
#    # generates points from surface : val = 2.0*xp**3 + 1.0*(xp**2)*(yp) + 3.0*(xp)*(yp**2) + 4*xp*yp + 3*xp + yp + 10 
#    python ./surface_generator.py > test.txt
# 
#    # fit 3 order polynomial:
#    python ./fit_poly_3d.py test.txt --order=3 
# 
#    # check if fitted polynomial is the same as generated :
#    Fitted polynomial p_n(x,y) =  10.00000000*(x**0)*(y**0) +  1.00000000*(x**0)*(y**1) +  0.00000000*(x**0)*(y**2) +  0.00000000*(x**0)*(y**3) +  3.00000000*(x**1)*(y**0) +  4.00000000*(x**1)*(y**1) +  
#                                   3.00000000*(x**1)*(y**2) +  0.00000000*(x**2)*(y**0) +  1.00000000*(x**2)*(y**1) +  2.00000000*(x**3)*(y**0)
#    
#    # plot fitted surface :
#    python ./plot_scatter_3d.py fitted_vs_data_order03.txt --vmin=0 --vmax=20
#    save image as plot.png
# 
#    # plot data :
#    python ./plot_scatter_3d.py fitted_vs_data_order03.txt --vmin=0 --vmax=20
#
#    # plot residuals :
#    python ./plot_scatter_3d.py fitted_vs_data_order03.txt --vmin=-4 --vmax=+4
#    
#    # compare results to a template :
#    diff plot.png diff template/plot_fitted_surface.png
#    # png images can differ due to different version of matplotlib, python etc.
#    diff fitted_order03.txt template/fitted_order03.txt
#    diff fitted_vs_data_order03.txt template/fitted_vs_data_order03.txt
#    diff test.txt template/test.txt
#
######################################################################################################################## 
import numpy as np
import os
import sys
import scipy.linalg
import copy
from optparse import OptionParser,OptionGroup
import re

import matplotlib as m
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid') # in python2 was : seaborn-whitegrid')

def parse_options():
   usage="Usage: %prog [options]\n"
   usage+='\tFit 2D surface to data files in a text file with values X Y Z\n'
   parser = OptionParser(usage=usage,version=1.00)
   parser.add_option('--vmin','--min_z','--min_value',dest="vmin",default=0.00, help="Vmin value for colorbar [default %]",type="float")
   parser.add_option('--vmax','--max_z','--max_value',dest="vmax",default=20.00, help="Vmax value for colorbar [default %]",type="float")
   parser.add_option('--order','--poly_order','--polynomial_order',dest="polynomial_order",default=7, help="Polynomial order [default %]",type="int")
   parser.add_option('--image_size','--size',dest="image_size",default=8192, help="Image size [default %]",type="int")
   parser.add_option('--ncols','--n_columns','--num_columns',dest="ncols",default=10, help="Number of columns in a file [default %]",type="int")
   parser.add_option('--verb','--verbose','--debug_level',dest="verbose",default=0, help="Verbosity level [default %]",type="int")
   parser.add_option('--no_files','--no_savefiles','--dont_save_files','--no_outputfiles',action="store_false",dest="save_files",default=True, help="Do not save results to text files just return then from the function [default %]")
   
   (options, args) = parser.parse_args()

   return (options, args)



def read_text_file( filename , verbose=0, ncols=10 ) :
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
            calconst = float(words[2+0])
         
            x_list.append(x)
            y_list.append(y)
            calconst_list.append(calconst)
            
      file.close()      
   else :
      print("WARNING : empty or non-existing file %s" % (filename))

   print("READ %d values from file %s" % (len(x_list),filename))
   
   return (x_list,y_list,calconst_list)

def plot_scatter( filename , vmin=0.00, vmax=20.00 ) :   
   (x_list,y_list,calconst_list) = read_text_file( filename )
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
#   plt.pcolor(x, y, colors, cmap=cm, vmin=-4, vmax=4)
#   plt.pcolor(x, y, colors, cmap=cm)
#   plt.loglog()
   plt.xlabel('X pixel')
   plt.ylabel('Y pixel')


   # https://matplotlib.org/stable/gallery/shapes_and_collections/scatter.html
   # plt.scatter(x, y, c=colors, s=sizes, alpha=0.3, cmap=cm )
   plt.scatter(x, y, c=colors, s=sizes, alpha=1.0, cmap='rainbow', vmin=vmin, vmax=vmax ) # cmap='viridis')
   plt.colorbar();  # show color scale   
   plt.show()

########################################################################################################################################
# Calculates polynomial value for list of points x,y using coefficients in poly_coeff (order of polynomial is n)
########################################################################################################################################
def calc_polynonial( x , y , poly_coeff, n ) :
   out_val = 0.00   
   n_params = len( poly_coeff )
   param_index = 0

   for p in range(0,n+1) :   
      # for q in range(0,p+1) : # q goes from 0 to p   
      for q in range(0,n-p+1 ) :
         if param_index >= n_params :
            print("ERROR in code : trying to print parameter %d when there are only %d" % (param_index,n_params))
            
         # polynomial_string += (" %.8f x^%d y^%d + " % (a[param_index],p,q))   
         val = poly_coeff[param_index]*(x**p)*(y**q)
         out_val = out_val + val
         param_index += 1
         
   return out_val

########################################################################################################################################
# RETURNS list of (a_pq,p,q) where a_pq is polynomial coefficient with power x^p*y^q
########################################################################################################################################
def get_polynonial( poly_coeff, n ) :
   n_params = len( poly_coeff )
   param_index = 0
   out_list = []

   for p in range(0,n+1) :   
      # for q in range(0,p+1) : # q goes from 0 to p   
      for q in range(0,n-p+1 ) :
         if param_index >= n_params :
            print("ERROR in code : trying to print parameter %d when there are only %d" % (param_index,n_params))
            
         # polynomial_string += (" %.8f x^%d y^%d + " % (a[param_index],p,q))   
         a_list = [poly_coeff[param_index] , p , q]
         
         out_list.append( a_list )
         
         param_index += 1
                  
         
   return out_list


########################################################################################################################################
# Calculates polynomial values using list of coefficients and exponents in the format as in the function get_polynonial
########################################################################################################################################
def calc_polynonial_list( x , y , poly_coeff ) :
   out_val = 0.00   
   n_params = len( poly_coeff )
   
   for param_index in range(0,n_params): 
      a_pq = poly_coeff[param_index][0] # a_pq
      p = poly_coeff[param_index][1]    # x^p
      q = poly_coeff[param_index][2]    # x^q
      
      val = a_pq*(x**p)*(y**q)
      out_val = out_val + val

   return out_val


########################################################################################################################################
# calculate derivatives (to check if they are indeed = 0 )
########################################################################################################################################
def calc_derivatives( x_list, y_list, z_list, poly_coeff, n ) :      
   len_data = len(z_list)
   n_params = len( poly_coeff )
   param_index = 0

   print("Calculating derivatives by a_pq:")
   for p in range(0,n+1) :   
      # for q in range(0,p+1) : # q goes from 0 to p   
      for q in range(0,n-p+1) :
         if param_index >= n_params :
            print("ERROR in code : trying to print parameter %d when there are only %d" % (param_index,n_params))
          
         # calculate derivative over a_pq
         deriv_value = 0.00            
         for k in range(0,len_data) :
             xk = x_list[k]
             yk = y_list[k]
             
             param_index2 = 0                          
             sum = 0.00
             for i in range(0,n+1) :
                for j in range(0,n-i+1) :
                   if param_index >= n_params :
                      print("ERROR in code : trying to print parameter %d when there are only %d" % (param_index,n_params))
                   
                   sum += poly_coeff[param_index]*(xk**(i))*(yk**(j))
                   
             deriv_value += ( sum - z_list[k] )*(xk**(p))*(yk**(q))
             
         
         print("dChi2/da_%d%d = %.8f" % (p,q,deriv_value))
                   

################################################################################################################################################
# Wrapper function reading a specified text file and calling the main fitting function 
# Chi2 = Sum_k=0^N { (p(x_k,y_k) - D_k ) ^ 2 }            
################################################################################################################################################
def fit_poly( filename , ncols=10, image_size=8192, polynomial_order=7, save_files=True, verbose=0 ) :
   (x_list,y_list,z_list) = read_text_file( filename, ncols=ncols )
   print("Read %d data points from file %s" % (len(x_list),filename))
         
   return fit_poly_base( x_list, y_list, z_list, image_size=image_size, polynomial_order=polynomial_order, save_files=save_files, verbose=verbose )
   
      
################################################################################################################################################
# Main fitting function :
#   Input : lists of x , y , z values 
################################################################################################################################################
def fit_poly_base( x_list, y_list, z_list , image_size=8192, polynomial_order=7, save_files=True, verbose=0 ) :
   # (x_list,y_list,z_list) = read_text_file( filename, ncols=options.ncols )
   x_list_original = copy.copy(x_list)
   y_list_original = copy.copy(y_list)
   
   
   image_size_x = image_size
   image_size_y = image_size
   x_c = image_size_x / 2.00
   y_c = image_size_y / 2.00

   if image_size is None or image_size <= 0 :
      image_size_x = max(x_list) 
      image_size_y = max(y_list)

      x_c = ( min(x_list) + max(x_list) ) / 2.00
      y_c = ( min(y_list) + max(y_list) ) / 2.00

   
   len_data = len(x_list)

   # shift to be around the image centre :   
   for i in range(0,len_data) :
      x_list[i] = ( x_list[i] - x_c ) / ( x_c )
      y_list[i] = ( y_list[i] - y_c ) / ( y_c )
   
   print("Fitting 3D surface to %d data points" % (len_data))
   
   n = polynomial_order   
   n_equations = 0 
   n_params = 0
   for p in range(0,n+1) :   
      for q in range(0,n-p+1) :
         print("%d : a_%d%d x^%d * y^%d" % (n_params,p,q,p,q))
         n_equations += 1
         n_params += 1

   
   # n_equations = (n+1)*(n+2)/2
   # n_params = (n+1)*(n+2)/2
   # example for n=3 (x^3 etc) it will be 4*5/2 = 10 parameters and equations 
   rhs = np.zeros(n_equations)
   lhs = {} # will have coeffients for n_equations 
   
   print("Fitting %d order polynomial -> %d parameters and %d equations" % (n,n_params,n_equations))
   
   # calculate derivatives by a_pq
   eq_index = 0 
   for p in range(0,n+1) :   
      # for q in range(0,p+1) : # q goes from 0 to p 
      for q in range(0,n-p+1) :
         if eq_index >= n_equations :
            print("ERROR in code : trying to calculate derivatives for equation %d whilst number of equations is %d" % (eq_index,n_equations))
            sys.exit(-1)
      
         # RHS :
         for k in range(0,len_data) :
            rhs[eq_index] = rhs[eq_index] + z_list[k]*(x_list[k])**(p)*(y_list[k])**(q)

         # LHS :
         coeff = np.zeros(n_params)   
         param_index = 0 
         for i in range(0,n+1) :
            # for j in range(0,i+1) :
            for j in range(0,n-i+1):
               if param_index >= n_params :
                  print("ERROR in code : trying to calculate coefficient at parameter %d whilst number of parameters is %d" % (param_index,n_params))
                  sys.exit(-1)
 
               # calculate coefficient at a_ij :           
               for k in range(0,len_data) :
                  coeff[param_index] = coeff[param_index] + (x_list[k])**(i+p)*(y_list[k])**(j+q)

               param_index += 1

         key = "a_%d%d" % (p,q)   
         lhs[eq_index] = copy.copy(coeff)
         eq_index += 1 
  
   print("\n\nEquations:")
#   for j in range(0,n_equations) :
   eq_index = 0 
   for p in range(0,n+1) :   
      # for q in range(0,p+1) : # q goes from 0 to p   
      for q in range(0,n-p+1):
         if eq_index >= n_equations :
             print("ERROR in code : trying to print equation %d whilst number of equations is %d" % (eq_index,n_equations))
             sys.exit(-1)

      
         key = "a_%d%d" % (p,q)
         line = ("dChi^2/d%s : " % key)
         
         param_index = 0
         for i in range(0,n+1) :
            for j in range(0,n-i+1):
               if param_index >= n_params :
                  print("ERROR in code : trying to calculate coefficient at parameter %d whilst number of parameters is %d" % (param_index,n_params))
                  sys.exit(-1)

               sign = "+"
               if lhs[eq_index][param_index] < 0 or i==0:
                  sign = ""
               line += ("%s%.8f*a_%d%d " % (sign,lhs[eq_index][param_index],i,j))
               
               param_index += 1
#         if lhs[j][i] < 0 :
#            prev_sign = -1
#         if i < (n+2) :
#            line += "+ "
         
         print("%s = %.8f" % (line,rhs[j]))
         eq_index += 1
      
      
            
   # solve equations :
   arrays = []
   for a in lhs.keys() :
      arrays.append( lhs[a] )
   lhs_eq = np.stack( arrays )
   print("%s" % (lhs_eq))
   
   a = np.linalg.solve(lhs_eq, rhs)
   print("Polynomial coefficients :")
   param_index = 0
   polynomial_string = ""
   for p in range(0,n+1) :   
      # for q in range(0,p+1) : # q goes from 0 to p   
      for q in range(0,n-p+1) :
         if param_index >= n_params :         
            print("ERROR in code : trying to print parameter %d when there are only %d" % (param_index,n_params))
            sys.exit(-1)
      
         print("\t a_%d%d = %.8f" % (p,q,a[param_index]))
         polynomial_string += (" %.8f*(x**%d)*(y**%d) + " % (a[param_index],p,q))
         param_index += 1 

   print("\n\nFitted polynomial p_n(x,y) = %s" % (polynomial_string))
   
   # check if ok solution :
   ok = np.allclose(np.dot(lhs_eq, a), rhs)
   print("Solution ok = %s" % (ok))

   out_f = None
   if save_files :
      outfile = ("fitted_vs_data_order%02d.txt" % n)   
      out_f = open(outfile,"w")
      out_f.write("# X  Y  FIT   DATA  DATA-FIT\n")
   else :
      print("WARNING : saving output files is not required")
      
   print("\n\nFitted values:")
   chi2 = 0 
   for i in range(0,len_data) :
      # calc_polynonial
      val = calc_polynonial( x_list[i] , y_list[i] , a, n )
      if verbose > 0 :
         print("%.3f %.3f  %.8f  vs. %.8f" % (x_list[i],y_list[i],z_list[i],val))
      
      if out_f is not None :
         line = "%.3f %.3f %.8f %.8f %.8f\n" % (x_list_original[i],y_list_original[i],val,z_list[i],(z_list[i]-val))
         out_f.write( line )
      
      chi2 += (val - z_list[i])**2 
   
   print("\n\nchi2 = %.8f\n" % chi2)
   if out_f is not None :
      out_f.close()

   if save_files :
      print("Saving fitted surface")   
      size = image_size
      step = 10
   
      outfile2 = ("fitted_order%02d.txt" % (n))
      out_f = open(outfile2,"w")
      out_f.write("# X  Y  FIT \n")
      out_f.write("# X,Y steps %d pixels\n" % step)
      for y in range(0,size,step) :
         if verbose > 0 :
            print("Progress y = %d" % (y))
         for x in range(0,size,step) :
            yp = ( y - y_c ) / y_c 
            xp = ( x - x_c ) / x_c 
         
            val = calc_polynonial( xp, yp, a , n )
            line = "%.3f %.3f %.8f\n" % (x,y,val)
            out_f.write( line )
         
          
      out_f.close()   
   else :
      print("WARNING : saving output files is not required")

   # calculate and show derivatives :
   calc_derivatives( x_list, y_list, z_list, a, n )

   # format coefficients into a list and return
   coeff_out = get_polynonial( a, n )
   
   return (True,coeff_out,a)

if __name__ == '__main__':
   filename = "mean_stokes_I_2axis_gleamcal.txt"
   if len(sys.argv) > 1:
      filename = sys.argv[1]

   (options, args) = parse_options()

   print("#################################################################")
   print("PARAMETERS :")
   print("#################################################################")
   print("Input file  = %s" % (filename))
   print("vmin - vmax = %.4f - %.4f" % (options.vmin,options.vmax))
   print("Polynomial order = %d" % (options.polynomial_order))
   print("N columns in input file = %d" % (options.ncols))
   print("#################################################################")
      
   # (x_list,y_list,z_list) = read_text_file( filename )
   (fit_ok,polynomial_coeff_list,coeff_only_list) = fit_poly( filename, ncols=options.ncols, image_size=options.image_size, polynomial_order=options.polynomial_order, save_files=options.save_files, verbose=options.verbose )
     
#   plot_scatter( filename , vmin=options.vmin, vmax=options.vmax )   
      
      


