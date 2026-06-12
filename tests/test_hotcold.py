"""Tests for hotcold() Bézier resampling (issue #2)."""

import numpy as np
import pytest

from bipolar import (
    _grayscale_axis_coordinate_rgb,
    _ratquad_bezier_rgb,
    _resample_uniform_grayscale_axis,
    hotcold,
)


def _colormap_rgb(cmap, n):
    return cmap(np.linspace(0, 1, n))[:, :3]


def _grayscale_axis_step_cv(rgb):
    """Coefficient of variation of |Δm| with m = (R+G+B)/3."""
    m = _grayscale_axis_coordinate_rgb(rgb)
    dm = np.abs(np.diff(m))
    if dm.size == 0 or dm.mean() == 0:
        return float("inf")
    return float(dm.std() / dm.mean())


def _control_points(neutral):
    n = neutral
    if 0 <= n <= 0.5:
        return (
            (0, 1, 1),
            (0, 0, 1),
            (n, n, n),
            (1, 0, 0),
            (1, 1, 0),
        )
    return (
        (0, 0, 1),
        (0, 1, 1),
        (n, n, n),
        (1, 1, 0),
        (1, 0, 0),
    )


def _uniform_t_hotcold_rgb(neutral, weight, lutsize):
    """Legacy uniform-t Bézier sampling (pre issue #2 fix)."""
    data = _control_points(neutral)
    p0 = np.asarray(data[2], dtype=float)
    p_mid1 = np.asarray(data[1], dtype=float)
    p_end1 = np.asarray(data[0], dtype=float)
    p_mid2 = np.asarray(data[3], dtype=float)
    p_end2 = np.asarray(data[4], dtype=float)
    n_half = lutsize // 2
    t = np.linspace(0.0, 1.0, n_half)
    rgb1 = _ratquad_bezier_rgb(p0, p_mid1, p_end1, weight, t)
    rgb2 = _ratquad_bezier_rgb(p0, p_mid2, p_end2, weight, t)
    return np.concatenate((rgb1[1:][::-1], rgb2))


@pytest.mark.parametrize("neutral", [1 / 3, 0.1, 0.9])
@pytest.mark.parametrize("weight", [1.0, 4.0])
def test_hotcold_grayscale_axis_more_uniform_than_uniform_t(neutral, weight):
    """LUT steps should advance more evenly along the RGB grayscale axis."""
    lutsize = 256
    cmap = hotcold(lutsize=lutsize, neutral=neutral, weight=weight)
    fixed_rgb = _colormap_rgb(cmap, lutsize)
    naive_rgb = _uniform_t_hotcold_rgb(neutral, weight, lutsize)

    fixed_cv = _grayscale_axis_step_cv(fixed_rgb)
    naive_cv = _grayscale_axis_step_cv(naive_rgb)

    assert fixed_cv < naive_cv
    assert fixed_cv < 0.35


def test_resample_uniform_grayscale_axis_low_cv():
    """Internal resampler should yield near-uniform |Δm| on a dense Bézier."""
    data = _control_points(1 / 3)
    p0 = np.asarray(data[2], dtype=float)
    p_mid = np.asarray(data[1], dtype=float)
    p_end = np.asarray(data[0], dtype=float)
    t_dense = np.linspace(0.0, 1.0, 8192)
    rgb_dense = _ratquad_bezier_rgb(p0, p_mid, p_end, 4.0, t_dense)
    rgb = _resample_uniform_grayscale_axis(rgb_dense, 128)

    assert _grayscale_axis_step_cv(rgb) < 0.05


def test_hotcold_lut_size_and_endpoints():
    cmap = hotcold(lutsize=128, neutral=1 / 3)
    assert cmap.N == 128
    rgb = _colormap_rgb(cmap, 128)
    assert rgb.shape == (128, 3)
    assert np.all(rgb >= 0) and np.all(rgb <= 1)
