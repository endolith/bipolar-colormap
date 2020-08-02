# bipolar-colormap
Hot and cold colormap for diverging data

This started as a translation of [Bipolar Colormap by Ged Ridgway](http://www.mathworks.com/matlabcentral/fileexchange/26026) into Python.  The original had 4 different colormap regions:

* n < 0.0: Rainbow colormap
* n < 0.5: Diverging cyan - blue - dark - red - yellow
* n = 0.5: Sequential dark purple to bright yellow
* n > 0.5: Diverging blue - cyan - light - yellow - red

This only implements 2:

* n < 0.5: Diverging cyan - blue - dark - red - yellow
* n ≥ 0.5: Diverging blue - cyan - light - yellow - red

This is not a modern well-designed colormap; it's not perceptually uniform, does not have uniform lightness steps, and the endpoints are not equal lightness.  But it looks nice for some purposes.

## Removing halos

The original `bipolar()` had "halos" ([Mach bands](https://en.wikipedia.org/wiki/Mach_bands#In_computer_graphics)?) from [going out to the corners of the RGB cube and then making a right angle](https://flic.kr/p/dYGXSR):

![bipolar with halos marked by arrows](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/bipolar%20halos.png)

So I made a version [with Bézier curves through the RGB cube](https://flic.kr/p/e1bcFf) that is smoother and gets rid of the prominent bands, and called it `hotcold()`.  I would recommend this be used instead of `bipolar()`:

![hotcold with no halos](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/hotcold%20no%20halos.png)

It's still not perceptually uniform, but improved.  I think true perceptual uniformity (equally-spaced steps in perceptual colorspace) is overrated, but it would be nice to improve it to have uniform lightness steps, and maybe same-lightness endpoints.

## Examples

![bipolar colormaps of 0.0, 0.2, 0.4, 0.6, 0.8, 1.0 neutral](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/bipolar%20range.png)

![hotcold colormaps of 0.0, 0.2, 0.4, 0.6, 0.8, 1.0 neutral](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/hotcold%20range.png)

## Similar

Very similar colormap is [FireIce by Joseph Kirk](http://www.mathworks.com/matlabcentral/fileexchange/24870)

Comparisons with other conceptually-similar maps from [matplotlib](https://matplotlib.org/tutorials/colors/colormaps.html#diverging), [colorcet](https://colorcet.holoviz.org/#Samples), and [CMasher](https://cmasher.readthedocs.io/user/diverging.html):

![bipolar colormap vs iceburn, redshift, bkr, bjr](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/dark%20comparison.png)

![bipolar colormap vs CET_D10, cwr, CET_D9, coolwarm, bwr, RdBu, seismic, fusion](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/light%20comparison.png)

