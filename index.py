import math

import pyglet

from config import *

print(Points)


class Constants:
    def __init__(self):
        self.GRAVITATIONAL_CONSTANT = 6.673e-11


Toolbox = Constants()


def distance(object1: Point, object2: Point):
    dx = abs(object1.position[0] - object2.position[0])
    dy = abs(object1.position[1] - object2.position[1])
    d = math.sqrt((dx ** 2) + (dy ** 2))
    return d


def gravitational_acceleration(object1: Point, object2: Point):
    a = object1.mass
    b = object2.mass
    d = distance(object1, object2)
    G = Toolbox.GRAVITATIONAL_CONSTANT
    F = G * ((a * b) / (d ** 2))
    return F


def acceleration_norm(object1: Point, force):
    return force / object1.mass


def decompose_acceleration(acceleration: float, receiver: Point, actor: Point):
    dx = actor.position[0] - receiver.position[0]
    dy = actor.position[1] - receiver.position[1]
    return acceleration * math.cos(math.atan2(dy, dx)), acceleration * math.sin(math.atan2(dy, dx))


def add_to_history(point: Point):
    point.history.append(point.position.copy())
    if len(point.history) > point.historylength:
        point.history.pop(0)


def vector_norm(vector: list):
    return math.sqrt((vector[0] ** 2) + (vector[1] ** 2))


def velocity_change(A: Point, B: Point):
    deltaVel = decompose_acceleration(
        acceleration_norm(
            A,
            gravitational_acceleration(
                A,
                B)
        ),
        A,
        B)
    return deltaVel


def sum_of_forces(forces):
    x = 0
    y = 0
    for force in forces:
        x += round(force[0], 8)
        y += round(force[1], 8)
    return [x, y]


# Points = []
#  Uncomment any of the two simulations to try the sim !
# 1000km x 1000km orbit simulation over earth
# P1 = Point(1, [0, 1000e+3 + 6371e+3], [7350.20, 0], historysetting=True, historylength=65, granularity=8)
# P2 = Point(5.9724e+24, [0, 0], [0, 0], radius=6378e+3, color=(0, 193, 0))
# Points = [
#    P1, P2
# ]
# zoomLevel = 25000

# 3 body system test
# P3 = Point(1.5e+15, [500, 0], [0, -15], historysetting=False, historylength=50, granularity=1, color=(0, 255, 0),
#           historycolor=(50, 255, 50))
# P4 = Point(1.5e+15, [-500, 0], [0, 15], historysetting=False, historylength=50, granularity=1, color=(0, 0, 255),
#           historycolor=(50, 50, 255))
# P5 = Point(5, [0, 0], [0, 0], historysetting=True, historylength=50, granularity=0, color=(255, 0, 0),
#           historycolor=(255, 50, 50))
# P5 = Point(1.5e+15, [0, 500], [15, 0], color=(255, 0, 0), historysetting=False, historylength=50, granularity=1,
#           historycolor=(255, 50, 50))
# P6 = Point(1.5e+15, [0, -500], [-15, 0], color=(255, 0, 255), historysetting=False, historylength=50, granularity=1,
#           historycolor=(255, 50, 255))
# Points = [
#    P6,
#    P5,
#    P4,
#    P3
# ]
# zoomLevel = 10
#
windowLength, windowWidth = 1000, 1000
window = pyglet.window.Window(windowLength, windowWidth)

j = 0


@window.event
def on_draw():
    global j
    j += 1
    window.clear()

    for i in range(timeStep):
        allforces = []
        for pA in Points:
            forces = []
            for pB in Points:
                if pA == pB:
                    continue
                forces.append(velocity_change(pA, pB))
            ftot = sum_of_forces(forces)
            allforces.append(ftot)
        i = 0
        for p in Points:
            p.velocity[0] += round(allforces[i][0], 8)
            p.velocity[1] += round(allforces[i][1], 8)
            p.position[0] += p.velocity[0]
            p.position[1] += p.velocity[1]
            i += 1
    for p in Points:
        if p.granularity == 0:
            add_to_history(p)
        elif (j % p.granularity) == 0:
            add_to_history(p)
        pyglet.shapes.Circle(
            x=(windowLength / 2) + (p.position[0] / zoomLevel),
            y=(windowWidth / 2) + (p.position[1] / zoomLevel),
            radius=(p.radius / zoomLevel) if p.radius != 0 else 5,
            color=p.color
        ).draw()
        if p.historysetting:
            previous = []  # it's here to catch an impossible occurrence since pos IS p.history[0] on first iteration
            for pos in p.history:
                if pos == p.history[0]:
                    previous = pos
                # pyglet.shapes.Circle(
                #    x=(windowLength / 2) + (pos[0] / zoomLevel),
                #    y=(windowWidth / 2) + (pos[1] / zoomLevel),
                #    radius=1,
                #    color=(255, 0, 255)
                # ).draw()
                pyglet.shapes.Line(
                    x=(windowLength / 2) + (pos[0] / zoomLevel),
                    y=(windowWidth / 2) + (pos[1] / zoomLevel),
                    x2=(windowLength / 2) + (previous[0] / zoomLevel),
                    y2=(windowWidth / 2) + (previous[1] / zoomLevel),
                    width=2,
                    color=p.historycolor
                ).draw(),
                previous = pos


pyglet.app.run()
