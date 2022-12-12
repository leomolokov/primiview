import ezdxf

import sys

class Line():
    def __init__(self, atr):
        self.atr = atr
        self.coords = []

    def __str__(self):
        return f'{self.atr}'

    def read(self, file):
        self.coords.append(file.dxf.start.x)
        self.coords.append(file.dxf.start.y)
        self.coords.append(file.dxf.end.x)
        self.coords.append(file.dxf.end.y)

class Arc():
    def __init__(self, atr):
        self.atr = atr
        self.coords = []

    def __str__(self):
        return f'{self.atr}'

    def read(self, file):
        self.coords.append(file.start_point.x)
        self.coords.append(file.start_point.y)
        self.coords.append(file.end_point.x)
        self.coords.append(file.end_point.y)
        self.rad = file.dxf.radius

# class Poly():
#     def __init__(self):
#         self.atr
#         self.coords = []

class DxfData():
    def __init__(self):
        self.lines = []
        self.arcs = []
        self.polylines = []


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
                self.lines.append(Line(prim).read(prim))

            elif prim.dxftype() == "ARC":
                self.arcs.append(Arc(prim).read(prim))

            # elif prim.dxftype() == "LWPOLYLINE":
            #     # file.write(str(prim))
            #     for x in prim.lwpoints:
            #         # print(*prim.lwpoints)
            #         # file.write(str(x))
            #         self.polylines.append(str(x))


    def print_data_into_txt(self):
        gen_txt = open(self.txtPath, 'a')

        for line in self.lines:
            gen_txt.write(line.atr + '\n')
            for i in range(4):
                gen_txt.write(line.coords[i] + '\t')
                if i == -1:
                    gen_txt.write(line.coords[i] + '\n')
            # gen_txt.write(line[0] + '\n')
            # gen_txt.write(line[1] + '\t')
            # gen_txt.write(line[2] + '\t')
            # gen_txt.write(line[3] + '\t')
            # gen_txt.write(line[4] + '\n')

        for arc in self.arcs:
            gen_txt.write(arc[0] + '\n')
            gen_txt.write(arc[1] + '\t')
            gen_txt.write(arc[2] + '\t')
            gen_txt.write(arc[3] + '\t')
            gen_txt.write(arc[4] + '\t')
            gen_txt.write(arc[5] + '\n')

        # for poly in self.polylines:
            # gen_txt.write(str(x))

        gen_txt.close()

    def define_dimes(self): #defines dimensions (profile) of a figure
        xs = []
        ys = []

        # for point in self.points:
        #     xs.append(self.)
        #     ys.append(point.coords[1])

        height = max(xs) - min(xs)
        width = max(ys) - min(ys)

        return height, width

    def define_extremums(self):
        xs = []
        ys = []

        # for point in self.points:
        #     xs.append(self.)
        #     ys.append(point.coords[1])

        return max(xs), min(xs), max(ys), min(ys)