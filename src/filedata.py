import ezdxf

import sys

class Line():
    def __init__(self, file):
        self.coords = []
        self.atr = file
        self.coords.append(file.dxf.start.x)
        self.coords.append(file.dxf.start.y)
        self.coords.append(file.dxf.end.x)
        self.coords.append(file.dxf.end.y)

    def __str__(self):
        return f'{self.atr}'

class Arc():
    def __init__(self, file):
        self.atr = file
        self.rad = file.dxf.radius
        self.start_point = file.start_point
        self.end_point = file.end_point
        self.start_angle = file.dxf.start_angle
        self.end_angle = file.dxf.end_angle
        self.center = [file.dxf.center[0], file.dxf.center[1]]

    def __str__(self):
        return f'{self.atr}'

class Circle():
    def __init__(self, file):
        self.atr = file
        self.center = file.dxf.center
        self.rad = file.dxf.radius

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


    def get_primitives_data(self, source_path, target_path):
        self.dxfPath = source_path
        self.txtPath = target_path

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
                # file.write(str(prim))
                # for x in prim.lwpoints:

                    # print(*prim.lwpoints)
                    # file.write(str(x))
                    # self.polylines.append(str(x))


    def print_data_into_txt(self):
        gen_txt = open(self.txtPath, 'w')

        for line in self.lines:
            gen_txt.write(str(line.atr) + '\n')
            for i in range(3):
                gen_txt.write(str(line.coords[i]) + '\t')
            gen_txt.write(str(line.coords[3]) + '\n')

        for arc in self.arcs:
            gen_txt.write(str(arc.atr) + '\n')
            for i in range(2):
                gen_txt.write(str(arc.center[i]) + '\t')
            gen_txt.write(str(arc.rad) + '\n')

        for circle in self.circles:
            gen_txt.write(str(circle.atr) + '\n')
            for i in range(2):
                gen_txt.write(str(circle.center[i]) + '\t')
            gen_txt.write(str(circle.rad) + '\n')

        for poly in self.polylines:
            # gen_txt.write(str(n[:2] for n in poly.lwpoints) + '\t')
            gen_txt.write(str(poly.atr) + '\n')
            for lwpoint in poly.lwpoints:
                gen_txt.write(str(lwpoint) + '\t')
            gen_txt.write('\n')
        gen_txt.close()

    def define_dimes(self): #defines dimensions (profile) of a figure
        xs = []
        ys = []

        for line in self.lines:
            xs.append(line.coords[0])
            ys.append(line.coords[1])

        for arc in self.arcs:
            xs.append(arc.start_point[0])
            xs.append(arc.end_point[0])
            ys.append(arc.start_point[1])
            ys.append(arc.end_point[1])

        for circle in self.circles:
            xs.append(circle.center[0] + circle.rad)
            xs.append(circle.center[0] - circle.rad)
            ys.append(circle.center[1] + circle.rad)
            ys.append(circle.center[1] - circle.rad)

        for poly in self.polylines:
            for n in poly.lwpoints:
                xs.append(n[0])
                ys.append(n[1])

        height = max(xs) - min(xs)
        width = max(ys) - min(ys)

        return height, width

    def define_extremums(self):
        xs = []
        ys = []

        for line in self.lines:
            xs.append(line.coords[0])
            ys.append(line.coords[1])

        self.lims = [min(xs), max(xs), min(ys), max(ys)]
        return self.lims