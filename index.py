import math
import pyglet

zoomLevel = 20000
historylength = 10000


# Main Program for the engine
# Well I hope?
# Let's just see where this goes ;)

# Constants for all the things and all
class Constants:
    def __init__(self):
        self.SPEED_OF_LIGHT = 2.9979e+8
        self.GRAVITATIONAL_CONSTANT = 6.673e-11
        self.TIME_STEP = 300  # SECONDS


Toolbox = Constants()


class Point:
    """"Defines a point in the 2D space of the engine by its mass and starting 2D coordinates"""

    def __init__(self,
                 mass: int,
                 startingposition: list,
                 startingvelocity: list,
                 radius: float = 0,
                 color: tuple = (255, 255, 255),
                 historysetting=False,
                 historylength=1000,
                 historycolor=(204, 0, 204),
                 predictionlength=0,
                 granularity=500
                 ):
        self.mass = mass
        self.position = startingposition
        self.velocity = startingvelocity
        self.radius = radius
        self.color = color
        self.history = []
        self.historysetting = historysetting
        self.historylength = historylength
        self.historycolor = historycolor
        self.predictionlength = predictionlength
        self.predictionhistory = [],
        self.granularity = round(granularity / Toolbox.TIME_STEP) if round(granularity / Toolbox.TIME_STEP) != 0 else 1


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


def addHistory(point: Point):
    point.history.append(point.position.copy())
    if len(point.history) > historylength:
        point.history.pop(0)


P1 = Point(1, [0, 1000e+3 + 6371e+3], [7350.20, 0], historysetting=True)
P2 = Point(5.9724e+24, [0, 0], [0, 0], radius=6378e+3, color=(0, 193, 0))

Points = [
    P1,
    P2
]  # "Sloppy" but should work somewhat for now

windowLength, windowWidth = 1000, 1000
window = pyglet.window.Window(windowLength, windowWidth)


def simulate(pA, pB):
    deltaVel = velocitydecomposition(
        accel(
            pA,
            gravitationalacceleration(
                pA,
                pB)
        ),
        pA,
        pB)
    pA.velocity[0] += deltaVel[0]
    pA.velocity[1] += deltaVel[1]
    pA.position[0] += pA.velocity[0]
    pA.position[1] += pA.velocity[1]


def predictionuupdate(point: Point):
    i = 0
    while i > len(point.predictionhistory):
        for pA in Points:
            for pB in Points:
                if pA == pB or pA.predictionlength == 0:
                    continue
                pAcopy = pA
                pBcopy = pB
                # simulate(pAcopy, pBcopy)


j = 0


@window.event
def on_draw():
    global j
    j += 1
    window.clear()

    for i in range(Toolbox.TIME_STEP):
        for pA in Points:
            for pB in Points:
                if pA == pB:
                    continue
                simulate(pA, pB)

    for p in Points:
        if p.granularity == 0:
            continue
        elif (j % p.granularity) == 0:
            addHistory(p)
        pyglet.shapes.Circle(
            x=(windowLength / 2) + (p.position[0] / zoomLevel),
            y=(windowWidth / 2) + (p.position[1] / zoomLevel),
            radius=(p.radius / zoomLevel) if p.radius != 0 else 5,
            color=p.color
        ).draw()
        if p.historysetting:
            for pos in p.history:
                if pos == p.history[0]:
                    previous = pos
                pyglet.shapes.Circle(
                    x=(windowLength / 2) + (pos[0] / zoomLevel),
                    y=(windowWidth / 2) + (pos[1] / zoomLevel),
                    radius=1,
                    color=(255, 0, 255)
                ).draw()
                pyglet.shapes.Line(
                    x=(windowLength / 2) + (pos[0] / zoomLevel),
                    y=(windowWidth / 2) + (pos[1] / zoomLevel),
                    x2=(windowLength / 2) + (previous[0] / zoomLevel),
                    y2=(windowWidth / 2) + (previous[1] / zoomLevel),
                    width=2,
                    color=(255, 0, 255)
                ).draw(),
                previous = pos


pyglet.app.run()
