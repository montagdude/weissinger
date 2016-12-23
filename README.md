#weissinger
The Weissinger-L method is an extension of Prandtl's lifting line theory to swept and tapered wings. It is also valid to lower aspect ratios than lifting line theory. The usual linear aerodynamics assumptions apply. This code is an implementation of the Weissinger-L method in Python. For a given wing geometry, it reports the lift and induced drag coefficients and creates plots of the lift distribution and wing shape.

You need:
* Python (tested with version 2.7.11, but earlier or later versions may also work)
* numpy (tested with version 1.11)
* matplotlib (tested with version 1.5.2)

If you use Linux, these are all likely available through your distribution's repositories. Alternatively, or if you use Windows, you can use a prepackaged Python suite such as Enthought Canopy, or Anaconda.

To run, edit inputs.py as desired and run in a terminal window/command prompt:
./run_weissinger.py (Linux, Mac OSX)
                 or
python.exe run_weissinger.py (Windows)

(In either case, it is assumed that Python has been installed in your executable path.)