import svgwrite
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="input file")
parser.add_argument("output_file", help="output_file")
args = parser.parse_args()


OFFSET = 50
dwg = svgwrite.Drawing(args.output_file, profile='tiny')

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
            circles.append(coords)
        elif len(coords) == 4: # segment
            min_x = min([min_x, *coords[::2]])
            min_y = min(min_y, *coords[1::2])
            segments.append((coords[:2], coords[2:]))
            
svg_group = dwg.g()
svg_group.translate(-min_x+OFFSET, -min_y+OFFSET)
svg_group.scale(1, -1)
dwg.add(svg_group)

for c in circles:
    svg_group.add(dwg.circle((c[0], c[1]), c[2],
                             stroke='black', stroke_width=1, fill="none"))    

for segment in segments:
    p1, p2 = segment    
    svg_group.add(dwg.line((p1[0], p1[1]), (p2[0], p2[1]),
                           stroke='black', stroke_width=1))    
    
dwg.save()
