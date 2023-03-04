import math
import pyglet

zoomLevel = 20000


# Main Program for the engine
# Well I hope?
# Let's just see where this goes ;)

# Constants for all the things and all
class Constants:
    def __init__(self):
        self.SPEED_OF_LIGHT = 2.9979e+8
        self.GRAVITATIONAL_CONSTANT = 6.673e-11
        self.TIME_STEP = 5  # SECONDS


Toolbox = Constants()


class Point:
    """"Defines a point in the 2D space of the engine by its mass and starting 2D coordinates"""

    def __init__(self, mass: int, startingposition: list, startingvelocity: list, radius: float):
        self.mass = mass
        self.position = startingposition
        self.velocity = startingvelocity
        self.radius = radius


def distance(object1: Point, object2: Point):
    dx = abs(object1.position[0] - object2.position[0])
    dy = abs(object1.position[1] - object2.position[1])
    d = math.sqrt((dx ** 2) + (dy ** 2))
    return d


def gravitationalacceleration(object1: Point, object2: Point):
    a = object1.mass
    b = object2.mass
    d = distance(object1, object2)
    G = Toolbox.GRAVITATIONAL_CONSTANT
    F = G * ((a * b) / (d ** 2))
    return F


def accel(object1: Point, force):
    return force / object1.mass


def velocitydecomposition(acceleration: float, receiver: Point, actor: Point):
    dx = actor.position[0] - receiver.position[0]
    dy = actor.position[1] - receiver.position[1]
    return acceleration * math.cos(math.atan2(dy, dx)), acceleration * math.sin(math.atan2(dy, dx))


P1 = Point(1, [0, 1000e+3 + 6371e+3], [7350.20, 0], 0)
P2 = Point(5.9724e+24, [0, 0], [0, 0], 6378e+3)
# print(P1)
# print(P1.mass)
# print(distance(P1, P2))

Points = [
    P1,
    P2
]  # "Sloppy" but should work somewhat

windowLength, windowWidth = 1000, 1000
window = pyglet.window.Window(windowLength, windowWidth)


@window.event
def on_draw():
    window.clear()
    for pA in Points:
        for pB in Points:
            if pA == pB:
                continue
            deltaVel = velocitydecomposition(
                accel(
                    pA,
                    gravitationalacceleration(pA, pB)
                ),
                pA,
                pB
            )
            pA.velocity[0] += deltaVel[0]
            pA.velocity[1] += deltaVel[1]
            pA.position[0] += pA.velocity[0]
            pA.position[1] += pA.velocity[1]
        pyglet.shapes.Circle(
            x=(windowLength / 2) + (pA.position[0] / zoomLevel),
            y=(windowWidth / 2) + (pA.position[1] / zoomLevel),
            radius=(pA.radius / zoomLevel) if pA.radius != 0 else 5,
            color=(255, 255, 255)
        ).draw()


pyglet.app.run()
