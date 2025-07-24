from __future__ import print_function
########################################################################################################################
#
# Developed by Marcin Sokolowski (marcin.sokolowski@curtin.edu.au) , version 1.00 , 2021-11
# generates a test surface and prints 3 columns (X,Y,Z) to a text file 
#
######################################################################################################################## 
import math

if __name__ == '__main__':
  
   size = 8192
   xc = float( size ) / 2.00
   yc = float( size ) / 2.00
   
   for y in range(0,size,100) :
      for x in range(0,size,100) :
         xp = float(x-xc)/xc
         yp = float(y-yc)/yc
         
         val = 2.0*xp**3 + 1.0*(xp**2)*(yp) + 3.0*(xp)*(yp**2) + 4*xp*yp + 3*xp + yp + 10
         print("%.4f %.4f %.8f" % (x,y,val))

