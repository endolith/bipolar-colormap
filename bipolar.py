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


def _ratquad_bezier_rgb(p0, p1, p2, w, t):
    """Rational quadratic Bézier in RGB; p* are shape (3,), t is 1d."""
    t = np.asarray(t, dtype=float)
    om = 1.0 - t
    den = om * om + 2.0 * w * om * t + t * t
    num = ((om[:, np.newaxis] ** 2) * p0
           + (2.0 * w * om[:, np.newaxis] * t[:, np.newaxis]) * p1
           + (t[:, np.newaxis] ** 2) * p2)
    return num / den[:, np.newaxis]


def _hsl_lightness_rgb(rgb):
    """HSL lightness L = (max(R,G,B) + min(R,G,B)) / 2; rgb is (n, 3)."""
    rgb = np.asarray(rgb, dtype=float)
    mx = np.max(rgb, axis=1)
    mn = np.min(rgb, axis=1)
    return (mx + mn) * 0.5


def _resample_uniform_hsl_lightness(rgb_dense, n_samples, rgb_mix=1e-4):
    """
    Resample the polyline through rgb_dense so LUT steps advance ~uniformly
    in cumulative |ΔL| along the path, where L is HSL lightness (the same L as
    in ``colorsys.rgb_to_hls``). Grays (R=G=B) lie on the RGB diagonal and have
    L=t. A small Euclidean RGB term keeps spacing well-defined where L is
    flat along saturated segments (uniform Bézier t still bunches there).
    """
    n_samples = int(n_samples)
    rgb_dense = np.asarray(rgb_dense, dtype=float)
    if n_samples < 2:
        raise ValueError('n_samples must be at least 2')
    if len(rgb_dense) < 2:
        return np.repeat(rgb_dense[:1], n_samples, axis=0)
    L = _hsl_lightness_rgb(rgb_dense)
    dL = np.abs(np.diff(L))
    drgb = np.linalg.norm(np.diff(rgb_dense, axis=0), axis=1)
    seg = dL + rgb_mix * drgb
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    s_max = cum[-1]
    if s_max <= 0:
        cum = np.concatenate([[0.0], np.cumsum(drgb)])
        s_max = cum[-1]
    targets = np.linspace(0.0, s_max, n_samples)
    return np.column_stack([
        np.interp(targets, cum, rgb_dense[:, 0]),
        np.interp(targets, cum, rgb_dense[:, 1]),
        np.interp(targets, cum, rgb_dense[:, 2]),
    ])


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
    ...                     ((1, 1), 2/3),
    ...                     ):
    ...     surf = axs[ax].plot_surface(x, y, z, rstride=1, cstride=1,
    ...                                 vmax=abs(z).max(), vmin=-abs(z).max(),
    ...                                 cmap=bipolar(neutral=neutral))
    >>>     axs[ax].set_title(f'{neutral:.3f}')
    ...     fig.colorbar(surf, ax=axs[ax])
    >>> plt.show()

    References
    ----------
    .. [1] Lehmann Manja, Crutch SJ, Ridgway GR et al. "Cortical thickness
        and voxel-based morphometry in posterior cortical atrophy and typical
        Alzheimer's disease", Neurobiology of Aging, 2009,
        doi:10.1016/j.neurobiolaging.2009.08.017

    """
    n = neutral
    if 0 <= n <= 0.5:
        if interp is None:
            # Seems to work well with dark neutral colors
            interp = 'linear'

        data = (
            (0, 1, 1),  # cyan
            (0, 0, 1),  # blue
            (n, n, n),  # dark neutral
            (1, 0, 0),  # red
            (1, 1, 0),  # yellow
        )
    elif 0.5 < n <= 1:
        if interp is None:
            # Seems to work better with bright neutral colors
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

    xi = np.linspace(0, 1, len(data))
    cm_interp = scipy.interpolate.interp1d(xi, data, axis=0, kind=interp)
    xnew = np.linspace(0, 1, lutsize)
    ynew = cm_interp(xnew)

    # Non-linear interpolation exceeds the RGB cube
    ynew = np.clip(ynew, 0, 1)

    return cm.colors.LinearSegmentedColormap.from_list('bipolar', ynew,
                                                       lutsize)


def hotcold(lutsize=256, neutral=1/3, interp=None, weight=1.0):
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
        Accepted for API compatibility with :func:`bipolar`; ignored here.
    weight : float, optional
        Rational Bézier weight on the middle control point for each smooth
        segment through the RGB cube (default 1). Larger values pull the path
        toward the middle control. Lookup rows are resampled from a dense
        uniform-`t` Bézier using ~uniform steps in cumulative HSL lightness
        change along the path (with a tiny RGB chord term where L is flat),
        instead of uniform `t` (which bunches samples toward the endpoints;
        see issue #2).

    Returns
    -------
    out : matplotlib.colors.LinearSegmentedColormap
        The resulting colormap object

    Examples
    --------
    >>> from mpl_toolkits.mplot3d import Axes3D
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from bipolar import hotcold

    >>> x = y = np.arange(-4, 4, 0.15)
    >>> x, y = np.meshgrid(x, y)
    >>> z = (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)

    >>> fig, axs = plt.subplots(2, 2, figsize=(12, 8),
    ...                         subplot_kw={'projection': '3d'})
    >>> for ax, neutral in (((0, 0), 1/3),  # Default
    ...                     ((0, 1), 0.1),  # Dark gray as neutral
    ...                     ((1, 0), 0.9),  # Light gray as neutral
    ...                     ((1, 1), 2/3),
    ...                     ):
    ...     surf = axs[ax].plot_surface(x, y, z, rstride=1, cstride=1,
    ...                                 vmax=abs(z).max(), vmin=-abs(z).max(),
    ...                                 cmap=hotcold(neutral=neutral))
    >>>     axs[ax].set_title(f'{neutral:.3f}')
    ...     fig.colorbar(surf, ax=axs[ax])
    >>> plt.show()

    References
    ----------
    .. [1] Lehmann Manja, Crutch SJ, Ridgway GR et al. "Cortical thickness
        and voxel-based morphometry in posterior cortical atrophy and typical
        Alzheimer's disease", Neurobiology of Aging, 2009,
        doi:10.1016/j.neurobiolaging.2009.08.017

    """
    n = neutral
    if 0 <= n <= 0.5:
        if interp is None:
            # Seems to work well with dark neutral colors
            interp = 'linear'

        data = (
            (0, 1, 1),  # cyan
            (0, 0, 1),  # blue
            (n, n, n),  # dark neutral
            (1, 0, 0),  # red
            (1, 1, 0),  # yellow
        )
    elif 0.5 < n <= 1:
        if interp is None:
            # Seems to work better with bright neutral colors
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

    if weight <= 0:
        raise ValueError('weight must be positive')

    p0 = np.asarray(data[2], dtype=float)
    p_mid1 = np.asarray(data[1], dtype=float)
    p_end1 = np.asarray(data[0], dtype=float)
    p_mid2 = np.asarray(data[3], dtype=float)
    p_end2 = np.asarray(data[4], dtype=float)

    n_half = lutsize // 2
    # Dense uniform t, then resample by cumulative |Δ HSL lightness| along the path
    # (uniform Bézier t bunches samples toward the endpoints on rational quadratics).
    n_dense = max(8192, lutsize * 64)
    t_dense = np.linspace(0.0, 1.0, n_dense)

    rgb1_dense = _ratquad_bezier_rgb(p0, p_mid1, p_end1, weight, t_dense)
    rgb2_dense = _ratquad_bezier_rgb(p0, p_mid2, p_end2, weight, t_dense)

    rgb1 = _resample_uniform_hsl_lightness(rgb1_dense, n_half)
    rgb2 = _resample_uniform_hsl_lightness(rgb2_dense, n_half)

    ynew = np.concatenate((rgb1[1:][::-1], rgb2))
    np.clip(ynew, 0.0, 1.0, out=ynew)

    return cm.colors.LinearSegmentedColormap.from_list('hotcold', ynew,
                                                       lutsize)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def func3(x, y):
        return (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)

    # Make these smaller to increase the resolution
    dx, dy = 0.02, 0.02
    plt.figure(figsize=(8, 6))

    x = np.arange(-3.0, 3.0001, dx)
    y = np.arange(-3.0, 3.0001, dy)
    X, Y = np.meshgrid(x, y)

    Z = func3(X, Y)
    cmap = hotcold(neutral=1/3, interp='linear', lutsize=2048)
    plt.pcolor(X, Y, Z, cmap=cmap, vmax=abs(Z).max(), vmin=-abs(Z).max())
    plt.colorbar()
    plt.axis([-3, 3, -3, 3])
    plt.tight_layout()
    plt.show()
