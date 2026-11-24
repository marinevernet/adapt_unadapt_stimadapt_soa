import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from nilearn import plotting

# ==========================================
# Experiment 2: stimulation target and centres of the spheres (regions of interest of the SimNIBS simulation)
# on a glass brain (MNI152 template)
# ==========================================

# adapt_unadapt_stimadapt_soa is the parent of the analysis folder containing this script
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
figures_folder = os.path.join(project_folder, 'figures', 'stimulation')
os.makedirs(figures_folder, exist_ok=True)

# Name, MNI coordinates (mm), color, marker, marker size
# Colors: Okabe-Ito palette (colour-blind friendly)
stimulation_target = ('Stimulated area', (44, -54, 38), 'black', '*', 260)
sphere_centres = [
    ('rAG', (56.60, -57.69, 43.55), '#E69F00', 'o', 110),
    ('rSMG', (58.85, -29.00, 34.54), '#56B4E9', 'o', 110),
    ('rS1', (36.59, -27.50, 64.50), '#009E73', 'o', 110),
    ('rSTS', (62.53, -38.52, 7.95), '#D55E00', 'o', 110),
    ('rV1', (8.45, -79.01, 6.49), '#0072B2', 'o', 110),
    ('Right precuneus', (8.02, -52.50, 49.51), '#CC79A7', 'o', 110),
    ('lAG', (-54.53, -58.56, 43.54), '#999999', 'o', 110),
]
regions = [stimulation_target] + sphere_centres

# ************* Glass brain: left, back, right and top views *************

fig = plt.figure(figsize=(14, 4.2))
display = plotting.plot_glass_brain(None, display_mode='lyrz', figure=fig, axes=[0, 0, 0.82, 1])
for name, xyz, color, marker, size in regions[::-1]: # The stimulated area is drawn last, on top of the others
    display.add_markers([xyz], marker_color=color, marker_size=size, marker=marker, edgecolors='white', linewidths=0.8)
handles = [Line2D([0], [0], marker=marker, color='w', markerfacecolor=color, markeredgecolor='white',
                  markersize=15 if marker == '*' else 10, label='%s (%g, %g, %g)' %((name,) + xyz))
           for name, xyz, color, marker, size in regions]
fig.legend(handles=handles, loc='center left', bbox_to_anchor=(0.82, 0.5), frameon=False, fontsize=10, title='MNI coordinates')
fig.savefig(os.path.join(figures_folder, 'glass_brain_coordinates.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ************* Distance between the stimulated area and the centre of each sphere *************

print('Distance from the stimulated area %s:' %(str(stimulation_target[1])))
for name, xyz, color, marker, size in sphere_centres:
    print('  %s: %.1f mm' %(name, np.linalg.norm(np.array(stimulation_target[1]) - np.array(xyz))))
