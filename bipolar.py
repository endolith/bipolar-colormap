"""
Hot/cold colormap for diverging data.

Copyright 2012 endolith at gmail com
Copyright 2009 Ged Ridgway at gmail com

Translation and modification of
http://www.mathworks.com/matlabcentral/fileexchange/26026-bipolar-colormap

Based on Manja Lehmann's hand-crafted colormap for cortical visualisation
"""
import numpy as np
import scipy.interpolate
from matplotlib import cm


def bipolar(lutsize=256, neutral=1/3, interp=None):
    """
    Bipolar hot/cold colormap, with neutral central color.

    This colormap is meant for visualizing diverging data; positive
    and negative deviations from a central value.  It is similar to a "hot"
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
        is < 0.5, and from blue-cyan-neutral-yellow-red if `neutral` > 0.5.
        For shaded 3D surfaces, a `neutral` near 0.5 is better, because it
        minimizes luminance changes that would otherwise obscure shading cues
        for determining 3D structure.
        For 2D heat maps, a `neutral` near the 0 or 1 extremes is better, for
        maximizing luminance change and showing details of the data.
    interp : str or int, optional
        Specifies the type of interpolation.
        ('linear', 'nearest', 'zero', 'slinear', 'quadratic, 'cubic')
        or as an integer specifying the order of the spline interpolator
        to use. Default is 'linear' for dark neutral and 'cubic' for light
        neutral.  See `scipy.interpolate.interp1d`.

    Returns
    -------
    out : matplotlib.colors.LinearSegmentedColormap
        The resulting colormap object

    Notes
    -----
    If neutral is exactly 0.5, then a map which yields a linear increase in
    intensity when converted to grayscale is produced. This colormap should
    also be reasonably good for colorblind viewers, as it avoids green and is
    predominantly based on the purple-yellow pairing which is easily
    discriminated by the two common types of colorblindness. [2]_

    Examples
    --------
    >>> from mpl_toolkits.mplot3d import Axes3D
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from bipolar import bipolar

    >>> x = y = np.arange(-4, 4, 0.15)
    >>> x, y = np.meshgrid(x, y)
    >>> z = (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)

    >>> fig, axs = plt.subplots(2, 2, figsize=(12, 8),
    ...                         subplot_kw={'projection': '3d'})
    >>> for ax, neutral in (((0, 0), 1/3),  # Default
    ...                     ((0, 1), 0.1),  # Dark gray as neutral
    ...                     ((1, 0), 0.9),  # Light gray as neutral
    ...                     ((1, 1), 0.5),  # Grayscale-friendly colormap
    ...                     ):
    ...     surf = axs[ax].plot_surface(x, y, z, rstride=1, cstride=1,
    ...                                 vmax=abs(z).max(), vmin=-abs(z).max(),
    ...                                 cmap=bipolar(neutral=neutral))
    ...     fig.colorbar(surf, ax=axs[ax])
    >>> plt.show()

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
        if interp is None:
            # Seems to work well with dark neutral colors
            # cyan-blue-dark-red-yellow
            interp = 'linear'

        data = (
            (0, 1, 1),  # cyan
            (0, 0, 1),  # blue
            (n, n, n),  # dark neutral
            (1, 0, 0),  # red
            (1, 1, 0),  # yellow
        )
    elif n >= 0.5:
        if interp is None:
            # Seems to work better with bright neutral colors
            # blue-cyan-light-yellow-red
            # Produces bright yellow or cyan rings otherwise
            interp = 'cubic'

        data = (
            (0, 0, 1),  # blue
            (0, 1, 1),  # cyan
            (n, n, n),  # light neutral
            (1, 1, 0),  # yellow
            (1, 0, 0),  # red
        )
    else:
        raise ValueError('n must be 0.0 < n < 1.0')

    xi = np.linspace(0, 1, np.size(data, 0))
    cm_interp = scipy.interpolate.interp1d(xi, data, axis=0, kind=interp)
    xnew = np.linspace(0, 1, lutsize)
    ynew = cm_interp(xnew)

    # No form of interpolation works without this, but that means the
    # interpolations are not working right.
    ynew = np.clip(ynew, 0, 1)

    return cm.colors.LinearSegmentedColormap.from_list('bipolar', ynew,
                                                       lutsize)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def func3(x, y):
        return (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)

    # Make these smaller to increase the resolution
    dx, dy = 0.05, 0.05

    x = np.arange(-3.0, 3.0001, dx)
    y = np.arange(-3.0, 3.0001, dy)
    X, Y = np.meshgrid(x, y)

    Z = func3(X, Y)
    plt.pcolor(X, Y, Z, cmap=bipolar(neutral=1./3, interp='linear'),
               vmax=abs(Z).max(), vmin=-abs(Z).max())
    plt.colorbar()
    plt.axis([-3, 3, -3, 3])
    plt.show()
