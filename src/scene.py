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
            # for current, next in zip(poly.lwpoints[::2], poly.lwpoints[1::2]):
                if current[4] == 0:
                    axes.add_line(Line2D([current[0], next[0]],
                                         [current[1], next[1]],
                                         color='g',
                                         lw=1.5))

                else:
                    polyarc_rad = abs(current[4] + 1 / current[4]) * math.sqrt((next[0] - current[0]) ** 2 + (next[1] - current[1]) ** 2) / 4
                    # polyarc_center = [(((1+current[4])**2)*current[0]/(4*current[4]) - ((1-current[4])**2)*next[0]/(4*current[4])),
                    #                   (((1+current[4])**2)*current[1]/(4*current[4]) - ((1-current[4])**2)*next[1]/(4*current[4]))]

                    # cx = (0.25/current[4])*(((1+current[4])**2)*current[0] - ((1-current[4])**2)*next[0])
                    # cy = (0.25/current[4])*(((1+current[4])**2)*current[1] - ((1-current[4])**2)*next[1])

                    # cx = (((1+current[4]) ** 2) * current[0] - ((1-current[4]) ** 2) * next[0]) / (4 * current[4])
                    # cy = (((1+current[4]) ** 2) * current[1] - ((1-current[4]) ** 2) * next[1]) / (4 * current[4])


                    cx = current[0] - polyarc_rad * math.cos(4 * math.atan(current[4]))
                    cy = current[1] - polyarc_rad * math.sin(4 * math.atan(current[4]))
                    # bulge = current[4]
                    # print(bulge)

                    start_angle = (4 * math.atan2(current[0], current[1])) * 180 / math.pi
                    end_angle = (4 * math.atan2(next[0], next[1])) * 180 / math.pi
                    # if current[4] <= 0:
                    #     temp = start_angle
                    #     start_angle = end_angle
                    #     end_angle = temp
                    axes.add_patch(Arc((cx, cy),
                                       width=2 * polyarc_rad,
                                       height=2 * polyarc_rad,
                                       theta1=start_angle,
                                       theta2=end_angle,
                                       color='g',
                                       lw=1.5,
                                       fill=False,
                                       alpha=1))

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