#!/usr/bin/env python

from __future__ import division
import scipy
from matplotlib import cm

def bipolar(lutsize=256, n=0.333, interp=[]):
    """
    %bipolar: symmetric/diverging/bipolar colormap, with neutral central color.
    %
    % Usage: cm = bipolar(m, neutral, interp)
    %  neutral is the gray value for the middle of the colormap, default 1/3.
    %  m is the number of rows in the colormap, defaulting to copy the current
    %    colormap, or the colormap that MATLAB defaults for new figures.
    %  interp is the method used to interpolate the colors, see interp1.
    %
    % The colormap goes from cyan-blue-neutral-red-yellow if neutral is < 0.5
    % (the default) and from blue-cyan-neutral-yellow-red if neutral > 0.5.
    %
    % If neutral is exactly 0.5, then a map which yields a linear increase in
    % intensity when converted to grayscale is produced (as derived in
    % colormap_investigation.m). This colormap should also be reasonably good
    % for colorblind viewers, as it avoids green and is predominantly based on
    % the purple-yellow pairing which is easily discriminated by the two common
    % types of colorblindness. For more details on this, see Brewer (1996):
    % http://www.ingentaconnect.com/content/maney/caj/1996/00000033/00000002/art00002
    % 
    % Examples:
    %  surf(peaks)
    %  cmx = max(abs(get(gca, 'CLim')));
    %  set(gca, 'CLim', [-cmx cmx]);
    %  colormap(bipolar)
    %
    %  imagesc(linspace(-1, 1,201)) % symmetric data, if not set symmetric CLim
    %  colormap(bipolar(201, 0.1)) % dark gray as neutral
    %  axis off; colorbar
    %  pause(2)
    %  colormap(bipolar(201, 0.9)) % light gray as neutral
    %  pause(2)
    %  colormap(bipolar(201, 0.5)) % grayscale-friendly colormap
    %
    % See also: colormap, jet, interp1, colormap_investigation, dusk
    % dusk is a colormap like bipolar(m, 0.5), in Oliver Woodford's real2rgb:
    %  http://www.mathworks.com/matlabcentral/fileexchange/23342
    %
    % Copyright 2009 Ged Ridgway at gmail com
    % Based on Manja Lehmann's hand-crafted colormap for cortical visualisation
    
    """
    if n < 0.5:
        if not interp:
            interp = 'linear' # seems to work well with dark neutral colors  cyan-blue-dark-red-yellow
       
        _data = (
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

        _data = (
            (0, 0, 1), # blue
            (0, 1, 1), # cyan
            (n, n, n), # light neutral
            (1, 1, 0), # yellow
            (1, 0, 0), # red
        )
    else:
        raise ValueError('n must be 0.0 < n < 1.0')
    
    xi = linspace(0, 1, size(_data, 0))
    cm_interp = scipy.interpolate.interp1d(xi, _data, axis=0, kind=interp)
    xnew = linspace(0, 1, lutsize)
    ynew = cm_interp(xnew)
    
    # No form of interpolation works without this, but that means the interpolations are not working right.
    ynew = clip(ynew, 0, 1)
    
    return cm.colors.LinearSegmentedColormap.from_list('bipolar', ynew, lutsize)

if __name__ == "__main__":
    
    from pylab import *
    
    def func3(x,y):
        return (1- x/2 + x**5 + y**3)*exp(-x**2-y**2)
        
    # make these smaller to increase the resolution
    dx, dy = 0.05, 0.05
    
    x = arange(-3.0, 3.0001, dx)
    y = arange(-3.0, 3.0001, dy)
    X,Y = meshgrid(x, y)
    
    #plot the colorbar with luminance, then adjust it to the opposite of coolwarm
    
    Z = func3(X, Y)
    #imshow(Z, vmax=abs(Z).max(), vmin=-abs(Z).max(), cmap=bipolar(n=1./3, interp='linear'))
    #figure()
    pcolor(X, Y, Z, cmap=bipolar(n=1./3, interp='linear'), vmax=abs(Z).max(), vmin=-abs(Z).max())
    colorbar()
    axis([-3,3,-3,3])

    show()
    