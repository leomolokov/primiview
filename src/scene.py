import math
from numpy import (array, dot, arccos)
from numpy.linalg import norm


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

    def polyarc_center(self, current, next, rad):
        #https://www.afralisp.net/archive/lisp/Bulges1.htm
        x = (current[0] + next[0]) / 2
        y = (current[1] + next[1]) / 2
        # if not an arc or a halfcircle - the center is the center of the chord
        if current[4] == (0 or 1 or (-1)):
            cx, cy = x, y
        else:
            # d = math.sqrt((next[0] - current[0]) ** 2 + (next[0] - current[0]) ** 2)  # It's a chord. A distance between start- and endpoint of a polyarc
            d = math.hypot(next[0] - current[0], next[1] - current[1])
            q = math.sqrt((rad ** 2) - (d / 2) ** 2)  # Apothem. This line starts at the center and is perpendicular to the chord
            a = math.atan(abs(current[4])) * 4  # Included arc angle (theta)
            if current[4] > 0:
                if a > math.pi:
                    cx = x - q * (current[1] - next[1]) / d
                    cy = y - q * (next[0] - current[0]) / d
                else:
                    cx = x + q * (current[1] - next[1]) / d
                    cy = y + q * (next[0] - current[0]) / d
            else:
                if a > math.pi:
                    cx = x + q * (current[1] - next[1]) / d
                    cy = y + q * (next[0] - current[0]) / d
                else:
                    cx = x - q * (current[1] - next[1]) / d
                    cy = y - q * (next[0] - current[0]) / d
        return [cx, cy]

    def angle_between_vectors(self, start_point1, end_point1, start_point2, end_point2):
        """takes start and end points of plain vectors. returns angle between them in grad"""
        u1 = array([end_point1[0] - start_point1[0], end_point1[1] - start_point1[1]])
        v = array([end_point2[0] - start_point2[0], end_point2[1] - end_point2[1]])
        c1 = dot(u1, v) / norm(u1) / norm(v)  # Cosinus of the angle
        angle = arccos(c1) * 180 / math.pi
        return angle

    def draw_lines(self, axes):
        from matplotlib.lines import Line2D
        from matplotlib.patches import Arc, Circle

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
                    center = self.polyarc_center(current, next, polyarc_rad)
                    start_angle = self.angle_between_vectors(center, current, [0, 0], [1, 0])
                    end_angle = self.angle_between_vectors(center, next, [0, 0], [1, 0])
                    axes.add_patch(Arc((center[0], center[1]),
                                       width=2 * polyarc_rad,
                                       height=2 * polyarc_rad,
                                       theta1=start_angle,
                                       theta2=end_angle,
                                       color='g',
                                       lw=1.5,
                                       fill=False,
                                       alpha=1))

            if poly.closed_flag == 1:
                axes.add_line(Line2D([poly.lwpoints[0][0], poly.lwpoints[-1][0]],
                                     [poly.lwpoints[0][1], poly.lwpoints[-1][1]],
                                     color='g',
                                     lw=1.5))

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