#!/usr/bin/env python

"""
Copyright 2012 endolith at gmail com
Copyright 2009 Ged Ridgway at gmail com

Translation and modification of
http://www.mathworks.com/matlabcentral/fileexchange/26026-bipolar-colormap

Based on Manja Lehmann's hand-crafted colormap for cortical visualisation
"""

from __future__ import division
import scipy
from matplotlib import cm
from numpy import linspace, size, clip, dstack, concatenate


# rename to hotcold
def bipolar(lutsize=1024, neutral=0.333, weight=1, interp=[]):
    """
    Bipolar hot/cold colormap, with neutral central color.

    This colormap is meant for visualizing diverging data; positive
    and negative deviations from a central value.  It is similar to a
    blackbody colormap for positive values, but with a complementary
    "cold" colormap for negative values.

    Parameters
    ----------
    lutsize : int
        The number of elements in the colormap lookup table. (Default is 256.)
    neutral : float
        The gray value for the neutral middle of the colormap.  (Default is
        1/3.)
        The colormap goes from cyan-blue-neutral-red-yellow if neutral
        is < 0.5, and from blue-cyan-neutral-yellow-red if neutral > 0.5.
        For shaded 3D surfaces, an `n` near 0.5 is better, because it
        minimizes luminance changes that would otherwise obscure shading cues
        for determining 3D structure.
        For 2D heat maps, an `n` near the 0 or 1 extremes is better, for
        maximizing luminance change and showing details of the data.
    weight : float
        The weight of the Bezier curve at the red and blue points.  1 is a
        normal Bezier curve.  Greater than one gets closer to pure colors and banding, less than one does the opposite
    interp : str or int, optional
        Specifies the type of interpolation.
        ('linear', 'nearest', 'zero', 'slinear', 'quadratic, 'cubic')
        or as an integer specifying the order of the spline interpolator
        to use. Default is 'linear'.  See `scipy.interpolate.interp1d`.

    Returns
    -------
    out : matplotlib.colors.LinearSegmentedColormap
        The resulting colormap object

    Notes
    -----
    If neutral is exactly 0.5, then a map which yields a linear increase in
    intensity when converted to grayscale is produced. This colormap should
    also be reasonably good
    for colorblind viewers, as it avoids green and is predominantly based on
    the purple-yellow pairing which is easily discriminated by the two common
    types of colorblindness. [2]_

    Examples
    --------
    >>> from mpl_toolkits.mplot3d import axes3d
    >>> from matplotlib import cm
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from bipolar import bipolar

    >>> fig = plt.figure()
    >>> ax = fig.gca(projection='3d')
    >>> X, Y, Z = axes3d.get_test_data(0.05)
    >>> ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0.1,
    >>>                 cmap=bipolar(),
    >>>                 vmax=abs(Z).max(), vmin=-abs(Z).max())
    >>> fig.colorbar()
    >>> plt.show()
    >>> set_cmap(bipolar(201))
    >>> waitforbuttonpress()
    >>> set_cmap(bipolar(201, 0.1)) # dark gray as neutral
    >>> waitforbuttonpress()
    >>> set_cmap(bipolar(201, 0.9)) # light gray as neutral
    >>> waitforbuttonpress()
    >>> set_cmap(bipolar(201, 0.5)) # grayscale-friendly colormap

    References
    ----------
    .. [1] Lehmann Manja, Crutch SJ, Ridgway GR et al. "Cortical thickness
        and voxel-based morphometry in posterior cortical atrophy and typical
        Alzheimer's disease", Neurobiology of Aging, 2009,
        doi:10.1016/j.neurobiolaging.2009.08.017
    .. [2] Brewer, Cynthia A., "Guidelines for Selecting Colors for
        Diverging Schemes on Maps", The Cartographic Journal, Volume 33,
        Number 2, December 1996, pp. 79-86(8)
        http://www.ingentaconnect.com/content/maney/caj/1996/00000033/00000002/art00002

    """
    n = neutral
    if n < 0.5:
        if not interp:
            interp = 'linear' # seems to work well with dark neutral colors  cyan-blue-dark-red-yellow

        data = (
            (0, 1, 1), # cyan
            (0, 0, 1), # blue
            (n, n, n), # dark neutral
            (1, 0, 0), # red
            (1, 1, 0), # yellow
        )
    elif n >= 0.5:
        if not interp:
            interp = 'cubic' # seems to work better with bright neutral colors blue-cyan-light-yellow-red
            # produces bright yellow or cyan rings otherwise

        data = (
            (0, 0, 1), # blue
            (0, 1, 1), # cyan
            (n, n, n), # light neutral
            (1, 1, 0), # yellow
            (1, 0, 0), # red
        )
    else:
        raise ValueError('n must be 0.0 < n < 1.0')

    t = linspace(0, 1, lutsize/2)
#    t = t**(3)

    # Super ugly Bezier curve
    # Do 2, one for each half, from nnn to 100 and from 001 to nnn

    x1 = data[2][0]
    y1 = data[2][1]
    z1 = data[2][2]

    xc = data[1][0]
    yc = data[1][1]
    zc = data[1][2]

    x2 = data[0][0]
    y2 = data[0][1]
    z2 = data[0][2]

    w = weight

    r1 = ((1 - t)**2*x1 + 2*(1 - t)*t*w*xc + t**2*x2) / ((1 - t)**2 + 2*(1 - t)*t*w + t**2)
    g1 = ((1 - t)**2*y1 + 2*(1 - t)*t*w*yc + t**2*y2) / ((1 - t)**2 + 2*(1 - t)*t*w + t**2)
    b1 = ((1 - t)**2*z1 + 2*(1 - t)*t*w*zc + t**2*z2) / ((1 - t)**2 + 2*(1 - t)*t*w + t**2)

    x1 = data[2][0]
    y1 = data[2][1]
    z1 = data[2][2]

    xc = data[3][0]
    yc = data[3][1]
    zc = data[3][2]

    x2 = data[4][0]
    y2 = data[4][1]
    z2 = data[4][2]

    r2 = ((1 - t)**2*x1 + 2*(1 - t)*t*w*xc + t**2*x2) / ((1 - t)**2 + 2*(1 - t)*t*w + t**2)
    g2 = ((1 - t)**2*y1 + 2*(1 - t)*t*w*yc + t**2*y2) / ((1 - t)**2 + 2*(1 - t)*t*w + t**2)
    b2 = ((1 - t)**2*z1 + 2*(1 - t)*t*w*zc + t**2*z2) / ((1 - t)**2 + 2*(1 - t)*t*w + t**2)

    rgb1 = dstack((r1, g1, b1))[0]
    rgb2 = dstack((r2, g2, b2))[0]

    ynew = concatenate((rgb1[1:][::-1], rgb2))


    return cm.colors.LinearSegmentedColormap.from_list('bipolar', ynew, lutsize)

if __name__ == "__main__":

    def relative_luminance((R, G, B)):
        Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
        return Y

    from pylab import *

    dx, dy = 0.01, 0.01


    def func3(x,y):
        # Sinusoid clearly shows edges, bands, or halos in the colormap
        return sin(x) + sin(y)

    x = arange(-4.0, 4.0001, dx)
    y = arange(-4.0, 4.0001, dy)

    X,Y = meshgrid(x, y)

    Z = func3(X, Y)
    figure()
    im = imshow(Z, vmax=abs(Z).max(), vmin=-abs(Z).max(),
                origin='lower',
                extent=[-3, 3, -3, 3],
                cmap=bipolar(neutral=0, lutsize=1024), # my favorite
                )
    colorbar()

    show()
