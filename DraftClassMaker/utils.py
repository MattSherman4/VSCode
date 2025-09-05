
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

pos_titles = {'QB' : 'Quarterback', 'HB' : 'Runningback',
              'WR' : 'Wide Receiver', 'TE' : 'Tigh End',
              'OT' : 'Offensive Tackle', 'OG' : 'Offensive Guard',
              'C' : 'Center', 'EDGE' : 'Edge Rusher',
              'DT' : 'Defensive Tackle', 'MLB' : 'Middle Linebacker',
              'CB' : 'Cornerback', 'S' : 'Safety',
              'K' : 'Kicker', 'P' : 'Punter', 'LS' : 'Long Snapper'}


cmap = plt.cm.turbo_r(np.linspace(0, 0.95))
cmap = LinearSegmentedColormap.from_list("turbo_cust", cmap)
cmap_red = plt.cm.turbo(np.linspace(0.5, 0.95))
cmap_red = LinearSegmentedColormap.from_list("turbo_red", cmap_red)
cmap_blue = plt.cm.turbo_r(np.linspace(0.5, 0.95))
cmap_blue = LinearSegmentedColormap.from_list("turbo_blue", cmap_blue)

def combine_height_to_inches(height_list):
    height_list = [str(h) for h in height_list]
    return [float((int(h[0]) * 12) + (int(h[1:3])) + (int(h[3]) / 8)) if h != 'nan' else 'nan' for h in height_list]

def inches_to_combine_height(height_list):
    height_list = [float(h) for h in height_list]
    return [int(float(str(int(h) // 12) + str(int(h) % 12).zfill(2) + str((h - int(h)) * 8))) if str(h) != 'nan' else np.nan for h in height_list]