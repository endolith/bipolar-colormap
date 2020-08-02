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

I also have a version with Bézier curves that is smoother and gets rid of the prominent bands, which I will eventually merge into this repo alongside the existing one: https://gist.github.com/endolith/ef948b924abf289287bd  https://www.flickr.com/photos/omegatron/8534628384/  https://www.flickr.com/photos/omegatron/8533520357/ 

## Examples

![bipolar colormaps of 0.0, 0.2, 0.4, 0.6, 0.8, 1.0 neutral](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/bipolar%20range.png)

## Similar

Very similar colormap is [FireIce by Joseph Kirk](http://www.mathworks.com/matlabcentral/fileexchange/24870)

Comparisons with other conceptually-similar maps from [matplotlib](https://matplotlib.org/tutorials/colors/colormaps.html#diverging), [colorcet](https://colorcet.holoviz.org/#Samples), and [CMasher](https://cmasher.readthedocs.io/user/diverging.html):

![bipolar colormap vs iceburn, redshift, bkr, bjr](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/dark%20comparison.png)

![bipolar colormap vs CET_D10, cwr, CET_D9, coolwarm, bwr, RdBu, seismic, fusion](https://raw.githubusercontent.com/endolith/bipolar-colormap/master/examples/light%20comparison.png)

