class Point:
    """"Defines a point in the 2D space of the engine by its mass and starting 2D coordinates"""

    def __init__(self,
                 mass: float,
                 startingposition: list,
                 startingvelocity: list = [0, 0],
                 radius: float = 0,
                 color: tuple = (255, 255, 255),
                 historysetting=False,
                 historylength=50,
                 historycolor=(204, 0, 204),
                 granularity=5,
                 ):
        from config import timeStep
        self.mass = mass
        self.position = startingposition
        self.velocity = startingvelocity
        self.radius = radius
        self.color = color
        self.history = []
        self.historysetting = historysetting
        self.historylength = historylength
        self.historycolor = historycolor
        self.historyprecision = round(granularity / timeStep) if round(granularity / timeStep) != 0 else 1
