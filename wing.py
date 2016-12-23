from math import pi, tan

def slope(y2, y1, x2, x1): return (y2 - y1) / (x2 - x1)

class Wing:
  """ Class for swept, tapered, twisted wing """

  def __init__(self, span, root, tip, sweep, washout):
    self.span = span
    self.root = root
    self.tip = tip
    self.sweep = sweep
    self.washout = washout
    self.area = None
    self.aspect_ratio = None
    self.cbar = None

    self.compute_geometry()

  def compute_geometry(self):
    """ Computes area, aspect ratio, MAC """

    self.area = 0.5*(self.root + self.tip)*self.span
    self.aspect_ratio = self.span**2./self.area
    self.compute_mac()

  def compute_mac(self):
    """ Computes mean aerodynamic chord """

    yroot = 0.
    ytip = self.span/2.
    xroot = [0., self.root]
    xrootc4 = self.root/4.
    xtipc4 = xrootc4 + self.span/2.*tan(self.sweep*pi/180.)
    xtip = [xtipc4 - 0.25*self.tip, xtipc4 + 0.75*self.tip]

    mt = slope(xtip[0], xroot[0], ytip, yroot)
    mb = slope(xtip[1], xroot[1], ytip, yroot)
    bt = xroot[0]
    bb = xroot[1]

    self.cbar = 2./self.area * (1./3.*ytip**3.*(mb-mt)**2. +
                                ytip**2.*(mb-mt)*(bb-bt) + ytip*(bb-bt)**2.)

  def plot(self, ax):

    yroot = 0.
    ytip = self.span/2.
    xroot = [0., self.root]
    xrootc4 = self.root/4.
    xtipc4 = xrootc4 + self.span/2.*tan(self.sweep*pi/180.)
    xtip = [xtipc4 - 0.25*self.tip, xtipc4 + 0.75*self.tip]

    x = [xroot[0], xtip[0], xtip[1], xroot[1], xtip[1], xtip[0], xroot[0]]
    y = [yroot,    ytip,    ytip,    yroot,    -ytip,   -ytip,    yroot]
    xrng = max(x) - min(x)
    yrng = self.span

    ax.plot(y, x, 'k')
    ax.set_xlabel('y')
    ax.set_ylabel('x')
    ax.set_xlim(-ytip-yrng/8., ytip+yrng/8.)
    ax.set_ylim(min(x)-xrng/8., max(x)+xrng/8.)
    ax.set_aspect('equal', 'datalim')
    ax.set_ylim(ax.get_ylim()[::-1])
