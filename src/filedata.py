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
            gen_txt.write(str(line.atr) + '\n')
            gen_txt.write(str(truncate(line.start.x, 2)) + '\t')
            gen_txt.write(str(truncate(line.start.y, 2)) + '\t')
            gen_txt.write(str(truncate(line.end.x, 2)) + '\t')
            gen_txt.write(str(truncate(line.end.y, 2)) + '\n')

        for arc in self.arcs:
            gen_txt.write(str(arc.atr) + '\n')
            gen_txt.write(str(truncate(arc.center.x, 2)) + '\t')
            gen_txt.write(str(truncate(arc.center.y, 2)) + '\t')
            gen_txt.write(str(truncate(arc.rad, 2)) + '\n')

        for circle in self.circles:
            gen_txt.write(str(circle.atr) + '\n')
            gen_txt.write(str(truncate(circle.center.x, 2)) + '\t')
            gen_txt.write(str(truncate(circle.center.y, 2)) + '\t')
            gen_txt.write(str(truncate(circle.rad, 2)) + '\n')

        for poly in self.polylines:
            gen_txt.write(str(poly.atr) + '\n')
            for lwpoint in poly.lwpoints:
                for coord in range(2):
                    gen_txt.write(str(truncate(lwpoint[coord], 2)) + '\t')
            gen_txt.write('\n')
        gen_txt.close()

    def print_prims_into_txt(self, target_path):
        self.txtPath = target_path

        gen_txt = open(self.txtPath, 'w')
        self.prev_point = []
        self.next_point = []

        for line in self.lines:
            if not self.prev_point:
                self.prev_point = [truncate(line.start.x, 2),
                                   truncate(line.start.y, 2),
                                   0]

            if self.prev_point != self.next_point:
                gen_txt.write('\t'.join(str(i) for i in self.prev_point))
                gen_txt.write('\n')

            self.next_point = [truncate(line.end.x, 2),
                               truncate(line.end.y, 2),
                               0]
            gen_txt.write('\t'.join(str(i) for i in self.next_point))
            gen_txt.write('\n')

        for arc in self.arcs:
            if not self.prev_point:
                self.prev_point = [truncate(arc.start_point.x, 2),
                                  truncate(arc.start_point.y, 2),
                                  0]

            if self.prev_point != self.next_point:
                gen_txt.write('\t'.join(str(i) for i in self.prev_point))
                gen_txt.write('\n')

            self.next_point = [truncate(arc.end_point.x, 2),
                              truncate(arc.end_point.y, 2),
                              truncate(arc.rad, 2)]
            gen_txt.write('\t'.join(str(i) for i in self.next_point))
            gen_txt.write('\n')

        for circle in self.circles:
            if not self.prev_point:
                self.prev_point = [truncate(circle.center.x, 2) + truncate(circle.rad, 2),
                                   truncate(circle.center.y, 2),
                                   0]

            if self.prev_point != self.next_point:
                gen_txt.write('\t'.join(str(i) for i in self.prev_point))
                gen_txt.write('\n')

            self.next_point = [self.prev_point[0],
                               self.prev_point[1],
                               truncate(circle.rad, 2)]
            gen_txt.write('\t'.join(str(i) for i in self.next_point))
            gen_txt.write('\n')

        for poly in self.polylines:
            for lwpoint in poly.lwpoints:
                if not self.prev_point:
                    self.prev_point = (truncate(lwpoint[0], 2),
                                       truncate(lwpoint[1], 2),
                                       0)

                if self.prev_point != self.next_point:
                    gen_txt.write('\t'.join(str(i) for i in self.prev_point))
                    gen_txt.write('\n')

                if lwpoint[4] == 0:
                    self.next_point = (truncate(lwpoint[0], 2),
                                       truncate(lwpoint[1], 2),
                                       0)

                elif lwpoint[4] != 0:
                    poly_rad = abs(lwpoint[4] + 1/lwpoint[4]) * math.sqrt((lwpoint[0] - self.prev_point[0]) ** 2 + (lwpoint[1] - self.prev_point[1]) ** 2) / 4
                    self.next_point = (truncate(lwpoint[0], 2),
                                       truncate(lwpoint[1], 2),
                                       truncate(poly_rad, 2))
                gen_txt.write('\t'.join(str(i) for i in self.next_point))
                gen_txt.write('\n')

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
        f.write(f'\t<g transform="scale=(1,-1)">\n\n')

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




    # def saveas_svg(self, target_path):
    #     import svgwrite
    #     import math
    #
    #     dwg = svgwrite.Drawing(target_path, profile='tiny')
    #
    #     def add_arc(svg, position, radius, rotation, start, end, color='white'):
    #         x0, y0 = position[0] + radius, position[1]
    #         x1, y1 = position[0] + radius, position[1]
    #         rad_start = math.radians(start % 360)
    #         rad_end = math.radians(end % 360)
    #         x0 -= (1 - math.cos(rad_start)) * radius
    #         y0 += math.sin(rad_start) * radius
    #         x1 -= (1 - math.cos(rad_end)) * radius
    #         y1 += math.sin(rad_end) * radius
    #
    #         args = {'x0': x0,
    #                 'y0': y0,
    #                 'x1': x1,
    #                 'y1': y1,
    #                 'xradius': radius,
    #                 'yradius': radius,
    #                 'ellipseRotation': 0,
    #                 'swap': 1 if end > start else 0,
    #                 'large': 1 if abs(start - end) > 180 else 0,
    #                 }
    #
    #         # 'a/A' params: (rx,ry x-axis-rotation large-arc-flag,sweep-flag x,y)+ (case dictates relative/absolute pos)
    #         path = """M %(x0)f,%(y0)f
    #                       A %(xradius)f,%(yradius)f %(ellipseRotation)f %(large)d,%(swap)d %(x1)f,%(y1)f
    #             """ % args
    #         arc = svg.path(d=path,
    #                        stroke='red',
    #                        fill='none')
    #         arc.rotate(rotation, position)
    #         svg.add(arc)
    #
    #     #https://svgwrite.readthedocs.io/en/latest/classes/drawing.html
    #     for line in self.lines:
    #         dwg.add(dwg.line(start=line.start[:2],
    #                          end=line.end[:2],
    #                          stroke=svgwrite.rgb(100, 0, 6, '%')))
    #
    #     #https://stackoverflow.com/questions/25019441/arc-pie-cut-in-svgwrite
    #     for arc in self.arcs:
    #         # addArc(dwg, current_group, p0=arc.start_point[:2], p1=arc.end_point[:2], radius=arc.rad)
    #         add_arc(dwg, arc.center[:2], arc.rad, 0, arc.start_angle, arc.end_angle, color='red')
    #
    #     for circle in self.circles:
    #         dwg.add(dwg.circle(center=circle.center[:2],
    #                            r=circle.rad,
    #                            stroke=svgwrite.rgb(100, 0, 6, '%'),
    #                            fill='none'))
    #
    #     for poly in self.polylines:
    #         # dwg.add(dwg.polyline(points=poly.lwpoints))
    #         self.polys = []
    #         for lwpoint in poly.lwpoints:
    #             self.polys.append(lwpoint[:2])
    #         dwg.add(dwg.polyline(points=self.polys,
    #                              stroke=svgwrite.rgb(100, 0, 6, '%'),
    #                              fill='none'))
    #
    #     dwg.save()