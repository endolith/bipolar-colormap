import matplotlib.cm as cm
import cmasher as cmr
from cmasher.utils import create_cmap_overview
import colorcet as cc
from bipolar import bipolar, hotcold

# Full range of bipolar plots
cmaps = []
for n in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cmap = bipolar(neutral=n)
    cmap.name = f'bipolar {n}'
    cmaps.append(cmap)

create_cmap_overview(cmaps, use_types=False, savefig='bipolar range.png',
                     plot_profile=True, sort=None, title="bipolar() range")

# Full range of hotcold plots
cmaps = []
for n in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    cmap = hotcold(neutral=n)
    cmap.name = f'hotcold {n}'
    cmaps.append(cmap)

create_cmap_overview(cmaps, use_types=False, savefig='hotcold range.png',
                     plot_profile=True, sort=None, title="hotcold() range")

# Bipolar vs other dark-centered hot-cold maps
cmaps = [('bipolar 0.0', bipolar(neutral=0)),
         ('hotcold 0.0', hotcold(neutral=0)),
         ('cmr.iceburn', cmr.iceburn),
         ('cmr.redshift', cmr.redshift),
         ('cc.bkr', cc.m_bkr),
         ('cc.bjr', cc.m_CET_D8),
         ('bipolar 0.4', bipolar(neutral=0.4)),
         ('hotcold 0.4', hotcold(neutral=0.4)),
         ]

for n, (name, cmap) in enumerate(cmaps):
    cmap.name = name
    cmaps[n] = cmap

create_cmap_overview(cmaps, use_types=False, savefig='dark comparison.png',
                     plot_profile=True, sort=None, title="Dark neutral maps")

# Bipolar vs other light-centered hot-cold maps
cmaps = [('bipolar 1.0', bipolar(neutral=1.0)),
         ('hotcold 1.0', hotcold(neutral=1.0)),
         ('cc.CET_D10', cc.m_CET_D10),
         ('cc.cwr', cc.m_cwr),
         ('cc.CET_D9', cc.m_CET_D9),
         ('cc.coolwarm', cc.m_coolwarm),
         ('cm.coolwarm', cm.coolwarm),
         ('cm.bwr', cm.bwr),
         ('cm.RdBu_r', cm.RdBu_r),
         ('cc.bwr', cc.m_CET_D1A),
         ('cm.seismic', cm.seismic),
         ('cmr.fusion_r', cmr.fusion_r),
         ]

for n, (name, cmap) in enumerate(cmaps):
    cmap.name = name
    cmaps[n] = cmap

create_cmap_overview(cmaps, use_types=False, savefig='light comparison.png',
                     plot_profile=True, sort=None, title="Light neutral maps")
