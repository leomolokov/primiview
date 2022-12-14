import ezdxf

import sys

from math_ops import *

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
        except IOError as e:
            raise RuntimeError(f"Not a DXF file or a generic I/O error.") from e
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted DXF file.")
            sys.exit(2)

        msp = doc.modelspace()

        for ins in msp.query("INSERT"):
            print(ins)

        for prim in msp.query("*"):
            if prim.dxftype() == "LINE":
                self.lines.append(Line(prim))

            elif prim.dxftype() == "ARC":
                self.arcs.append(Arc(prim))

            elif prim.dxftype() == "CIRCLE":
                self.circles.append(Circle(prim))

            elif prim.dxftype() == "LWPOLYLINE":
                self.polylines.append(Poly(prim))

    def print_dxf_into_txt(self, target_path):
        self.txtPath = target_path

        gen_txt = open(self.txtPath, 'w')

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
                self.prev_point = (truncate(lwpoint[0], 2),
                                   truncate(lwpoint[1], 2),
                                   0)

                if self.prev_point != self.next_point:
                    gen_txt.write('\t'.join(str(i) for i in self.prev_point))
                    gen_txt.write('\n')

        gen_txt.close()



    # def define_dimes(self): #defines dimensions (profile) of a figure
    #     xs = []
    #     ys = []
    #
    #     for line in self.lines:
    #         xs.append(line.coords[0])
    #         ys.append(line.coords[1])
    #
    #     for arc in self.arcs:
    #         xs.append(arc.start_point[0])
    #         xs.append(arc.end_point[0])
    #         ys.append(arc.start_point[1])
    #         ys.append(arc.end_point[1])
    #
    #     for circle in self.circles:
    #         xs.append(circle.center[0] + circle.rad)
    #         xs.append(circle.center[0] - circle.rad)
    #         ys.append(circle.center[1] + circle.rad)
    #         ys.append(circle.center[1] - circle.rad)
    #
    #     for poly in self.polylines:
    #         for n in poly.lwpoints:
    #             xs.append(n[0])
    #             ys.append(n[1])
    #
    #     height = max(xs) - min(xs)
    #     width = max(ys) - min(ys)
    #
    #     return height, width
    #
    # def define_extremums(self):
    #     xs = []
    #     ys = []
    #
    #     for line in self.lines:
    #         xs.append(line.coords[0])
    #         ys.append(line.coords[1])
    #
    #     self.lims = [min(xs), max(xs), min(ys), max(ys)]
    #     return self.lims

