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
        self.coords = []
        self.coords.append(file.start_point.x)
        self.coords.append(file.start_point.y)
        self.coords.append(file.end_point.x)
        self.coords.append(file.end_point.y)
        self.rad = file.dxf.radius
        self.start_angle = file.dxf.start_angle
        self.end_angle = file.dxf.end_angle
        self.center = [file.dxf.center[0], file.dxf.center[1]]

    def __str__(self):
        return f'{self.atr}'

class Poly():
    def __init__(self, file):
        self.atr = file
        self.lwpoints = file.lwpoints
        # for lwpoint in file.lwpoints:
            # self.lwpoints.append(lwpoint.)


class DxfData():
    def __init__(self):
        self.lines = []
        self.arcs = []
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
            # gen_txt.write(str(line.atr) + '\n')
            for i in range(3):
                gen_txt.write(str(line.coords[i]) + '\t')
            gen_txt.write(str(line.coords[3]) + '\n')

        for arc in self.arcs:
            # gen_txt.write(str(arc.atr) + '\n')
            for i in range(4):
                gen_txt.write(str(arc.coords[i]) + '\t')
            gen_txt.write(str(arc.rad) + '\n')

        # for poly in self.polylines:
            # gen_txt.write(str(x))

        gen_txt.close()

    def define_dimes(self): #defines dimensions (profile) of a figure
        xs = []
        ys = []

        for line in self.lines:
            xs.append(line.coords[0])
            ys.append(line.coords[1])

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