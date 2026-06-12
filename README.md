# bipolar-colormap

Hot and cold colormap for diverging data

## Citing this repository

GitHub shows APA and BibTeX from [`CITATION.cff`](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files) via **Cite this repository** on the repo home page.

For a **DOI** (recommended for long-term archival), use [Zenodo’s GitHub integration](https://help.zenodo.org/docs/github/): enable the integration for this repo, then publish a [GitHub Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) (or push a semver tag `vX.Y.Z`, e.g. `v0.1.0`, so the [release workflow](.github/workflows/release.yml) creates one). Zenodo archives each release and issues a version DOI. After the first Zenodo archive, add that DOI to the top-level `doi` field in `CITATION.cff` so citations include it.

Pushing a `vX.Y.Z` tag also runs a **PyPI** upload job using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (`id-token: write` and the `pypi` [GitHub environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)). Configure the project and workflow on PyPI before relying on it; until then the publish step fails while the GitHub Release still succeeds.

Continuous integration runs **pytest** and **Ruff** on Python 3.10–3.12 for pushes and pull requests (see [.github/workflows/ci.yml](.github/workflows/ci.yml)).

## Installation

The layout follows the idea of the [matplotlib colormap template](https://github.com/matplotlib/matplotlib-cmap-template) (single importable module) with [PEP 517](https://peps.python.org/pep-0517/) metadata in `pyproject.toml`, built with [Hatchling](https://hatch.pypa.io/latest/config/build/).

From a clone of this repository:

```bash
pip install .
```

Editable install while developing:

```bash
pip install -e ".[dev]"
```

Run tests locally:

```bash
pytest
```

The import name is still `bipolar` (`from bipolar import bipolar, hotcold`). Optional dependencies used by `examples/comparison.py`:

```bash
pip install ".[examples]"
```

This started as a translation of [Bipolar Colormap by Ged Ridgway](http://www.mathworks.com/matlabcentral/fileexchange/26026) into Python, which was inspired by (but not identical to) [Manja Lehmann's hand-crafted colormap for cortical visualisation](https://doi.org/10.1016/j.neurobiolaging.2009.08.017).  The original had 4 different colormap regions:

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
