import math

class Sketch():
    def initSketch(self, geodata):
        self.geodata = geodata


    def draw_grid(self, axes):
        axes.cla()
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.margins(0.05)
        axes.set_aspect("equal")
        axes.grid()
        axes.set_axisbelow(True)

    def draw_lines(self, axes):
        from matplotlib.lines import Line2D
        from matplotlib.patches import Arc, Polygon, Circle

        self.draw_grid(axes)

        for line in self.geodata.lines:
            axes.add_line(Line2D([line.start.x, line.end.x],
                                 [line.start.y, line.end.y],
                                 color='g',
                                 lw=1.5))

        for poly in self.geodata.polylines:
            for current, next in zip(poly.lwpoints[::], poly.lwpoints[1::]):
                if next[4] == 0:
                    axes.add_line(Line2D([current[0], next[0]],
                                         [current[1], next[1]],
                                         color='g',
                                         lw=1.5))

                else:
                    polyarc_rad = abs(next[4] + 1 / next[4]) * math.sqrt((next[0] - current[0]) ** 2 + (next[1] - current[1]) ** 2) / 4
                    polyarc_center = [((1+next[4])**2)*current[0]/(4*next[4]) - ((1-next[4])**2)*current[0]/(4*next[4]),
                                      ((1+next[4])**2)*current[1]/(4*next[4]) - ((1-next[4])**2)*current[1]/(4*next[4])]

                    axes.add_patch(Arc((polyarc_center[0], polyarc_center[1]),
                                       width=2 * polyarc_rad,
                                       height=2 * polyarc_rad,
                                       theta1=polyarc_rad,
                                       theta2=polyarc_rad,
                                       color='g',
                                       lw=1.5,
                                       fill=False,
                                       alpha=1))

            # axes.add_patch(Polygon([n[:2] for n in poly.lwpoints],
            #                        closed=True,
            #                        fill=False,
            #                        color='g',
            #                        alpha=1,
            #                        lw=1.5,
            #                        clip_on=False
            #                        ))

        for arc in self.geodata.arcs:
            axes.add_patch(Arc((arc.center.x, arc.center.y),
                               width=2*arc.rad,
                               height=2*arc.rad,
                               theta1=arc.start_angle,
                               theta2=arc.end_angle,
                               color='g',
                               lw=1.5,
                               fill=False,
                               alpha=1))

        for circle in self.geodata.circles:
            axes.add_patch(Circle((circle.center.x, circle.center.y),
                                  radius=circle.rad,
                                  color='g',
                                  fill=False,
                                  alpha=1))