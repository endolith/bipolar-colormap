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

Very similar colormap is [FireIce by Joseph Kirk](http://www.mathworks.com/matlabcentral/fileexchange/24870)

I want to make it smoother and get rid of the prominent bands.  Bezier curves work pretty well: https://www.flickr.com/photos/omegatron/8534628384/  https://www.flickr.com/photos/omegatron/8533520357/