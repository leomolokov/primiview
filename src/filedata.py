import ezdxf

import sys

from math_ops import *
import math

class Line():
    def __init__(self, file):
        self.coords = []
        self.atr = file
        self.start = vec3(file.dxf.start.x,
                          file.dxf.start.y,
                          file.dxf.start.z)
        self.end = vec3(file.dxf.end.x,
                        file.dxf.end.y,
                        file.dxf.end.z)

    def __str__(self):
        return f'{self.atr}'

class Arc():
    def __init__(self, file):
        self.atr = file
        self.rad = file.dxf.radius
        self.start_angle = file.dxf.start_angle
        self.end_angle = file.dxf.end_angle
        self.center = vec3(file.dxf.center.x,
                           file.dxf.center.y,
                           file.dxf.center.z)
        self.start_point = vec3(file.start_point.x,
                                file.start_point.y,
                                file.start_point.z)
        self.end_point = vec3(file.end_point.x,
                              file.end_point.y,
                              file.end_point.z)

    def __str__(self):
        return f'{self.atr}'

class Circle():
    def __init__(self, file):
        self.atr = file
        self.rad = file.dxf.radius
        self.center = vec3(file.dxf.center.x,
                           file.dxf.center.y,
                           file.dxf.center.z)

    def __str__(self):
        return f'{self.atr}'

class Poly():
    def __init__(self, file):
        self.atr = file
        self.lwpoints = file.lwpoints
        self.closed_flag = file.closed

    def __str__(self):
        return f'{self.atr}'

class DxfData():
    def __init__(self):
        self.lines = []
        self.arcs = []
        self.circles = []
        self.polylines = []
        self.lims = []
        self.halfprims = []


    def get_primitives_data(self, source_path):
        self.dxfPath = source_path

        try:
            doc = ezdxf.readfile(self.dxfPath)
        # except IOError as e:
        #     raise RuntimeError(f"Not a DXF file or a generic I/O error.") from e
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted DXF file.")
            sys.exit(2)

        msp = doc.modelspace()

        for ins in msp.query('INSERT'):
            ins.explode()

        for entity in msp.query('*'):
            if entity.dxftype() == "LINE":
                self.lines.append(Line(entity))

            elif entity.dxftype() == "ARC":
                self.arcs.append(Arc(entity))

            elif entity.dxftype() == "CIRCLE":
                self.circles.append(Circle(entity))

            elif entity.dxftype() == "LWPOLYLINE":
                self.polylines.append(Poly(entity))

    def print_dxf_into_txt(self, target_path):
        gen_txt = open(target_path, 'w')

        for line in self.lines:
            gen_txt.writelines(f'''{line.atr}
{line.start.x:.3} {line.start.y:.3}
{line.end.x:.3} {line.end.y:.3}\n''')

        for arc in self.arcs:
            gen_txt.writelines(f'''{arc.atr}
{arc.center.x:.3} {arc.center.y:.3} {arc.rad:.3}\n''')

        for circle in self.circles:
            gen_txt.writelines(f'''{circle.atr}
{circle.center.x:.3} {circle.center.y:.3} {circle.rad:.3}\n''')

        for poly in self.polylines:
            gen_txt.write(str(poly.atr) + '\n')
            for lwpoint in poly.lwpoints:
                for coord in range(2):
                    gen_txt.write(f'{lwpoint[coord]:.3} ')
            gen_txt.write('\n')
        gen_txt.close()

    def polyarc_rad(self, current, next):
        rad = 0 if current[4] == 0 else (abs(current[4] + 1 / current[4]) * math.sqrt((next[0] - current[0]) ** 2 + (next[1] - current[1]) ** 2) / 4)
        return rad

    def print_prims_into_txt(self, target_path):
        gen_txt = open(target_path, 'w')

        for line in self.lines:
            gen_txt.writelines(f'''{line.start.x:.3} {line.start.y:.3} 0
{line.end.x:.3} {line.end.y:.3} 0\n''')

        for arc in self.arcs:
            gen_txt.writelines(f'''{arc.start_point.x:.3} {arc.start_point.y:.3} 0
{arc.end_point.x:.3} {arc.end_point.y:.3} {arc.rad:.3}\n''')

        for circle in self.circles:
            #1st half(arc) of a circle
            gen_txt.writelines(f'''{(circle.center.x + circle.rad):.3} {circle.center.y:.3} 0
{(circle.center.x - circle.rad):.3} {circle.center.y:.3} {circle.rad:.3}\n''')
            # 2nd half(arc) of a circle
            gen_txt.writelines(f'''{(circle.center.x - circle.rad):.3} {circle.center.y:.3} 0
{(circle.center.x + circle.rad):.3} {circle.center.y:.3} {circle.rad:.3}\n''')

        for poly in self.polylines:
            pPoint = None
            for lwpoint in poly.lwpoints:
                if pPoint is not None:
                    rad = self.polyarc_rad(pPoint, lwpoint)
                    # rad = 0 if pPoint[4] == 0 else (abs(pPoint[4] + 1 / pPoint[4]) * math.sqrt((lwpoint[0] - pPoint[0]) ** 2 + (lwpoint[1] - pPoint[1]) ** 2) / 4)
                    gen_txt.writelines(f'''{pPoint[0]:.3f} {pPoint[1]:.3f} 0
{lwpoint[0]:.3f} {lwpoint[1]:.3f} {rad:.3f}\n''')
                pPoint = lwpoint
        gen_txt.close()

    def define_dimes(self): #defines dimensions (profile) of a figure
        xs = []
        ys = []

        for line in self.lines:
            xs.append(line.start.x)
            xs.append(line.end.x)
            ys.append(line.start.y)
            ys.append(line.end.y)

        for arc in self.arcs:
            xs.append(arc.center.x + arc.rad)
            xs.append(arc.center.x - arc.rad)
            ys.append(arc.center.y + arc.rad)
            ys.append(arc.center.y - arc.rad)

        for circle in self.circles:
            xs.append(circle.center.x + circle.rad)
            xs.append(circle.center.x - circle.rad)
            ys.append(circle.center.y + circle.rad)
            ys.append(circle.center.y - circle.rad)

        for poly in self.polylines:
            for n in poly.lwpoints:
                xs.append(n[0])
                ys.append(n[1])

        width = max(xs) - min(xs)
        height = max(ys) - min(ys)

        return width, height

    def define_extremums(self):
        xs = []
        ys = []

        for line in self.lines:
            xs.append(line.start.x)
            xs.append(line.end.x)
            ys.append(line.start.y)
            ys.append(line.end.y)

        for arc in self.arcs:
            xs.append(arc.center.x + arc.rad)
            xs.append(arc.center.x - arc.rad)
            ys.append(arc.center.y + arc.rad)
            ys.append(arc.center.y - arc.rad)

        for circle in self.circles:
            xs.append(circle.center.x + circle.rad)
            xs.append(circle.center.x - circle.rad)
            ys.append(circle.center.y + circle.rad)
            ys.append(circle.center.y - circle.rad)

        for poly in self.polylines:
            for n in poly.lwpoints:
                xs.append(n[0])
                ys.append(n[1])

        # lims = [min(xs), max(xs), min(ys), max(ys)]
        # return lims
        return min(xs), max(ys)

    def saveas_svg(self, target_path):
        minx, miny = self.define_extremums()
        width, height = self.define_dimes()
        f = open(f'{target_path}', mode='w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.writelines(['<svg version="1.1" width="100%" height="100%"\n',
                        f'\tviewBox="{minx} -{miny} {width} {height}"\n'
                        '\tbaseProfile="full"\n',
                        '\txmlns="http://www.w3.org/2000/svg"\n'
                        '\txmlns:xlink="http://www.w3.org/1999/xlink"\n',
                        '\txmlns:ev="http://www.w3.org/2001/xml-events">\n\n'])
        f.write(f'\t<g transform="scale(1,-1)">\n\n')

        for line in self.lines:
            f.write(f'\t\t<line x1="{line.start.x}" y1="{line.start.y}" x2="{line.end.x}" y2="{line.end.y}" stroke="red" stroke-width="2"/>\n\n')

        for arc in self.arcs:
            #https://stackoverflow.com/questions/5736398/how-to-calculate-the-svg-path-for-an-arc-of-a-circle
            # large_arc_flag = bool((arc.end_angle - arc.start_angle) % 360 > 180)
            large_arc_flag = 0 #arc is small
            sweep_flag = 1 #counter clockwise
            if (arc.end_angle - arc.start_angle) % 360 > 180:
                large_arc_flag = 1 #arc is large
            f.writelines([f'\t\t<path d="M {arc.start_point.x},{arc.start_point.y} A{arc.rad},{arc.rad}\n',
                          f'\t\t0 {large_arc_flag},{sweep_flag} {arc.end_point.x},{arc.end_point.y}"\n',
                          f'\t\tfill="none" stroke="red" stroke-width="2"/>\n\n'])

        for circle in self.circles:
            f.write(f'\t\t<circle cx="{circle.center.x}" cy="{circle.center.y}" r="{circle.rad}" fill="none" stroke="red" stroke-width="2"/>\n\n')

        if self.polylines:
            points = []
        for poly in self.polylines:
            for lwpoint in poly.lwpoints:
                points.append(lwpoint[:2])
            f.writelines([f'\t\t<polyline fill="none" stroke="red" stroke-width="10"\n',
                         f'\t\tpoints="'])
            for point in points:
                f.write(f'{point[0]}, {point[1]} ')
            f.write('"/>\n')

        f.write('\t</g>\n')
        f.write('</svg>')
        f.close()