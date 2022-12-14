from matplotlib.lines import Line2D

class Sketch():
    def initSketch(self, geodata):
        self.geo_data = geodata

    def draw_grid(self, axes):
        # axes.plot()
        axes.cla()
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.margins(0.05)
        axes.set_aspect("equal")
        axes.set_xlim(-30, 30)
        axes.set_ylim(-30, 30)
        axes.grid()


    def draw_lines(self, axes):
        self.draw_grid(axes)
        line = Line2D([0, 0], [5, 5], color='r')
        axes.add_line(line)

        # for segment in self.segments:
        #     self.
            # coord_link0 = int(segment.links[0])
            # coord_link1 = int(segment.links[1])
            # x0 = self.points[coord_link0].coords[0]
            # y0 = self.points[coord_link0].coords[1]
            # x1 = self.points[coord_link1].coords[0]
            # y1 = self.points[coord_link1].coords[1]
            # line = Line2D([x0, x1], [y0, y1], color='r')
            # axes.add_line(line)