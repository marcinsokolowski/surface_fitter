# surface_fitter
Developed by Marcin Sokolowski (marcin.sokolowski@curtin.edu.au) , version 1.00 , 2021-11
Fits a surface represented by a polynomial of an arbitrary order by calculating derivative over each cofficient, equaling them to zero and forming as many equations as many parameters
  
  Requirements :
     matplotlib
     scipy
     numpy

  Example usage and test :

     # generates points from surface : val = 2.0*xp**3 + 1.0*(xp**2)*(yp) + 3.0*(xp)*(yp**2) + 4*xp*yp + 3*xp + yp + 10 
     python ./surface_generator.py > test.txt
 
     # fit 3 order polynomial:
     python ./fit_poly_3d.py test.txt --order=3 
 
     # check if fitted polynomial is the same as generated :
     Fitted polynomial p_n(x,y) =  10.00000000*(x**0)*(y**0) +  1.00000000*(x**0)*(y**1) +  0.00000000*(x**0)*(y**2) +  0.00000000*(x**0)*(y**3) +  3.00000000*(x**1)*(y**0) +  4.00000000*(x**1)*(y**1) +  
                                   3.00000000*(x**1)*(y**2) +  0.00000000*(x**2)*(y**0) +  1.00000000*(x**2)*(y**1) +  2.00000000*(x**3)*(y**0)
    
     # plot fitted surface :
     python ./plot_scatter_3d.py fitted_vs_data_order03.txt --vmin=0 --vmax=20
  
     # plot data :
     python ./plot_scatter_3d.py fitted_vs_data_order03.txt --vmin=0 --vmax=20

     # plot residuals :
    python ./plot_scatter_3d.py fitted_vs_data_order03.txt --vmin=-4 --vmax=+4
     
  USAGE :
     python ./fit_poly_3d.py 3_COLUMN_TEXT_FILE_X_Y_Z.txt --order=3

     Options : 
        --order=3 : fits 3rd order polynomial, i.e. p(x,y) = a30 x^3 + a31 x^2 y^1 + a32 x^1 y^2 + a33 x^0 y^3 + a20 x^2 + a21 x^1 y^1 + a22 x^0 y^2 + a10 X^1 + a11 y^1 + a00
        --vmin    : minimum value on Z axis
        --vmax    : maximum value on Z axis
        --image_size : image size, default 8192, when set to 0 (--image_size=0) it will be automatically calculated as max(x)
        --verb    : verbosity level [default 0]
           
  OUTPUT FILES :
     For example for a 3rd order polynomial fit as in the example above :

       fitted_order03.txt         - ext file with fitted values, with higher resolution in X and Y (default step = 10 pixels), 3 columns : X Y FITTED_VALUE
       fitted_vs_data_order03.txt - text file with data and fitted surface 5 columns : X Y FITTED_VALUE DATA_VALUE RESIDUAL(=DATA-FIT)



