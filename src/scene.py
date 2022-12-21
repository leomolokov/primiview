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
        from matplotlib.patches import Arc, Polygon, Circle

        self.draw_grid(axes)

        for line in self.geodata.lines:
            axes.add_line(Line2D([line.coords[0], line.coords[2]],
                                 [line.coords[1], line.coords[3]],
                                 color='r'))

        for poly in self.geodata.polylines:
            axes.add_patch(Polygon([n[:2] for n in poly.lwpoints],
                                   closed=True,
                                   fill=False,
                                   color='b',
                                   alpha=1,
                                   edgecolor='b'))

        for arc in self.geodata.arcs:
            axes.add_patch(Arc((arc.center[0], arc.center[1]),
                               width=2*arc.rad,
                               height=2*arc.rad,
                               theta1=arc.start_angle,
                               theta2=arc.end_angle,
                               color='b',
                               fill=False,
                               alpha=1))

        for circle in self.geodata.circles:
            axes.add_patch(Circle((circle.center[0], circle.center[1]),
                                  radius=circle.rad,
                                  color='b',
                                  fill=False,
                                  alpha=1))