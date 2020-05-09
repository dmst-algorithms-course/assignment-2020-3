import matplotlib

import matplotlib.pyplot as plt

from matplotlib import collections  as mc
from matplotlib.patches import Circle

import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="input file")
parser.add_argument("output_file", help="output_file")
args = parser.parse_args()

min_x = sys.maxsize
max_x = -sys.maxsize
min_y = sys.maxsize
max_y = -sys.maxsize

circles = []
segments = []

with open(args.input_file) as input_file:
    for line in input_file:
        coords = [ float (x) for x in line.split() ]
        if len(coords) == 3: # circle
            min_x = min(min_x, coords[0]-coords[2])
            min_y = min(min_y, coords[1]-coords[2])
            max_x = max(max_x, coords[0]+coords[2])
            max_y = max(max_y, coords[1]+coords[2])            
            circles.append(Circle(coords[:2], coords[2],
                                  edgecolor='black', facecolor='none',
                                  linewidth=1))
        elif len(coords) == 4: # segment
            min_x = min([min_x, *coords[::2]])
            min_y = min(min_y, *coords[1::2])
            max_x = max([max_x, *coords[::2]])
            max_y = max(max_y, *coords[1::2])            
            segments.append((coords[:2], coords[2:]))

fig, ax = plt.subplots()
ax.set_xlim(min_x - 1, max_x + 1)
ax.set_ylim(min_y - 1, max_y + 1)
sc = mc.LineCollection(segments, colors='black', linewidths=1)
sc.set_capstyle('round')
ax.add_collection(sc)
cc = mc.PatchCollection(circles, match_original=True)
ax.add_collection(cc)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
if args.output_file:
    plt.savefig(args.output_file, dpi=300)
plt.show()
