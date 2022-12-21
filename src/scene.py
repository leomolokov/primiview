class Sketch():
    def initSketch(self, geodata):
        self.geodata = geodata

    def draw_grid(self, axes):
        axes.cla()
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.margins(0.05)
        axes.set_aspect("equal")
        axes.set_xlim(-30, 30)
        axes.set_ylim(-30, 30)
        axes.grid()

    # def draw_grid(self, axes, lims):
    #     self.lims = lims
    #
    #     axes.cla()
    #     axes.set_xlabel('X')
    #     axes.set_ylabel('Y')
    #     axes.margins(0.05)
    #     axes.set_aspect("equal")
    #     axes.set_xlim(lims[0], lims[1])
    #     axes.set_ylim(lims[2], lims[3])
    #     axes.grid()


    def draw_lines(self, axes):
        from matplotlib.lines import Line2D
        from matplotlib.patches import Arc

        self.draw_grid(axes)

        for line in self.geodata.lines:
            axes.add_line(Line2D([line.coords[0], line.coords[2]], [line.coords[1], line.coords[3]], color='r'))

        for poly in self.geodata.polylines:
            from matplotlib.patches import Polygon
            axes.add_patch(Polygon([n[:2] for n in poly.lwpoints], closed=True, fill=False, color='b', alpha=1))

        # for arc in self.geodata.arcs:
        #     arc_x = arc.center[0]
        #     arc_y = arc.center[1]
        #     arc_width = 1
        #     arc_height = 1
        #     arc_theta1 = arc.start_angle
        #     arc_theta2 = arc.end_angle
        #
        #     arc = arc.patches.Arc((arc_x, arc_y),
        #                                  arc_width,
        #                                  arc_height,
        #                                  theta1=arc_theta1,
        #                                  theta2=arc_theta2)
        #     axes.add_patch(arc)
        # arc.text(0.6, -0.3, "Arc", horizontalalignment="center")