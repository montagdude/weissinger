from math import sqrt, pi, cos, sin, tan
import numpy as np

eps = 1E-10

def l_function(lam, spc, y, n):
  """ Weissinger-L function, formulation by De Young and Harper.
      lam: sweep angle of quarter-chord (radians)
      spc: local span/chord
      y: y/l = y*
      n: eta/l = eta* """
 
  if abs(y-n) < eps:
    weissl = tan(lam)

  else:
    yp = abs(y)
    if n < 0.:
      weissl = sqrt((1.+spc*(yp+n)*tan(lam))**2. + spc**2.*(y-n)**2.) / \
                    (spc*(y-n) * (1.+spc*(yp+y)*tan(lam))) - 1./(spc*(y-n)) + \
                    2.*tan(lam) * sqrt((1.+spc*yp*tan(lam))**2. \
                                        + spc**2.*y**2.) / \
                    ((1.+spc*(yp-y)*tan(lam)) * (1.+spc*(yp+y)*tan(lam))) 
    else:
      weissl = -1./(spc*(y-n)) + sqrt((1.+spc*(yp-n)*tan(lam))**2. + \
                                       spc**2.*(y-n)**2.) / \
               (spc*(y-n) * (1.+spc*(yp-y)*tan(lam)))

  return weissl 

def weissinger_l(sp, root, tip, lam, tw, al, m):
  """ Weissinger-L method for a swept, tapered, twisted wing.
      sp: span
      root: chord at the root
      tip: chord at the tip
      lam: quarter-chord sweep (degrees)
      tw: twist of tip relative to root, +ve up (degrees)
      al: angle of attack (degrees) at the root
      m: number of points along the span (an odd number) """

  # Convert angles to radians
  lam = lam*pi/180.
  tw = tw*pi/180.
  al = al*pi/180.

  # Initialize solution arrays
  O = m+2
  phi   = np.zeros((m))
  y     = np.zeros((m))
  c     = np.zeros((m))
  spc   = np.zeros((m))
  twist = np.zeros((m))
  theta = np.zeros((O))
  n     = np.zeros((O))
  rhs   = np.zeros((m,1))
  b     = np.zeros((m,m))
  g     = np.zeros((m,m))
  A     = np.zeros((m,m))

  # Compute phi, y, chord, span/chord, and twist on full span
  for i in range(m):
    phi[i]   = (i+1)*pi/float(m+1)       #b[v,v] goes to infinity at phi=0
    y[i]     = cos(phi[i])               #y* = y/l
    c[i]     = root + (tip-root)*y[i]    #local chord
    spc[i]   = sp/c[i]                   #span/(local chord)
    twist[i] = abs(y[i])*tw              #local twist

  # Compute theta and n
  for i in range(O):
    theta[i] = i*pi/float(O-1)
    n[i]     = cos(theta[i])
  n0 = 1.
  phi0 = 0.
  nO1 = -1.
  phiO1 = pi

  # Construct the A matrix, which is the analog to the 2D lift slope
  for j in range(m):
    rhs[j,0] = al + twist[j]

    for i in range(m):
      if i == j: b[j,i] = float(m+1)/(4.*sin(phi[j]))
      else: b[j,i] = sin(phi[i]) / (cos(phi[i])-cos(phi[j]))**2. * \
            (1. - (-1.)**float(i-j))/float(2*(m+1))

      g[j,i] = 0.
      Lj0 = l_function(lam, spc[j], y[j], n0)
      LjO1 = l_function(lam, spc[j], y[j], nO1)
      fi0 = 0.
      fiO1 = 0.
      for mu in range(m):
        fi0 += 2./float(m+1) * (mu+1)*sin((mu+1)*phi[i])*cos((mu+1)*phi0)
        fiO1 += 2./float(m+1) * (mu+1)*sin((mu+1)*phi[i])*cos((mu+1)*phiO1)

      for r in range(O):
        Ljr = l_function(lam, spc[j], y[j], n[r])
        fir = 0.
        for mu in range(m):
          fir += 2./float(m+1) * (mu+1)*sin((mu+1)*phi[i])*cos((mu+1)*theta[r])
        g[j,i] += Ljr*fir;
      g[j,i] = -1./float(2*(O+1)) * ((Lj0*fi0 + LjO1*fiO1)/2. + g[j,i])

      if i == j: A[j,i] = b[j,i] + sp/(2.*c[j])*g[j,i]
      else: A[j,i] = sp/(2.*c[j])*g[j,i] - b[j,i]

  # Scale the A matrix
  A *= 1./sp 

  # Calculate ccl
  ccl = np.linalg.solve(A, rhs)

  # Add a point at the tip where the solution is known
  y = np.hstack((np.array([1.]), y))
  ccl = np.hstack((np.array([0.]), ccl[:,0]))
  c = np.hstack((np.array([tip]), c))
  twist = np.hstack((np.array([tw]), twist))

  # Return only the right-hand side (symmetry)
  nrhs = (m+1)/2+1
  y = y[0:nrhs]
  ccl = ccl[0:nrhs]

  # Sectional cl and induced angle of attack
  cl = np.zeros(nrhs)
  al_i = np.zeros(nrhs)
  for i in range(nrhs):
    cl[i] = ccl[i]/c[i]
    al_e = cl[i]/(2.*pi)
    al_i[i] = al + twist[i] - al_e

  # Integrate to get CL and CDi
  CL = 0.
  CDi = 0.
  area = 0.
  for i in range(1,nrhs):
    dA = 0.5*(c[i]+c[i-1]) * (y[i-1]-y[i])
    dCL = 0.5*(cl[i-1]+cl[i]) * dA
    dCDi = sin(0.5*(al_i[i-1]+al_i[i])) * dCL
    CL += dCL
    CDi += dCDi
    area += dA
  CL /= area
  CDi /= area

  return y, cl, ccl, al_i*180./pi, CL, CDi
