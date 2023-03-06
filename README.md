# 2D N-body physics simulation

This project is a 2D N-body physics simulation made because I was curious about
how ![Principia](https://github.com/mockingbirdnest/Principia#readme) worked, so I decided to replicate a few of its
most basic features.

## How it works

For every point in a system (the `Points` array), it calculates the forces exerted on it by other points. Then, using
the point's physical properties, it calculates the change in velocity and position and updates the system.
It has support for higher speeds, a lot of different systems and only has extremely marginal precision losses to nullify
floating point math imprecision.

## How to create a custom system

If you wish to create your custom system, simply modify the `config.py` file with whatever you want.

### `config.py` global variables

#### `timeStep`, integer

timeStep is basically how fast time passes.

A timeStep value of 1 still means the system is simulated at whatever the pyglet window is running at.
**If you have a 60Hz screen**, a timeStep value of 1 will run at 60x real speed.
A timeStep value of 10, will run at 600x real speed.

#### `dezoomLevel`, integer

This is how much scaled the window is.
If you have a dezoomLevel of 1, a pixel will be 1 meter.
If you have a dezoomLevel of 10, a pixel will be 10 meter.

#### `windowLength`, `windowWidth`, integers

Those two variables define the window's dimensions. They are set in pixels.

### The `Point` class

To define a point in the system, there is a Point class defined in `point.py`. It has attributes to define its
properties but also to view history for example.

#### `mass`, kilograms, integer (**mandatory**)

This parameter is fairly straightforward, it's the mass of the object in kilograms.

#### `startingposition`, meters, array of size 2 (**mandatory**)

This parameter is the starting position of the point in the system, where \[0,0\] is the center of the window.
The position is in meters.
Example :

```python
startingposition = [
    -300,
    300
]
```

#### `startingvelocity`, meters per second, array of size 2

This parameter is the starting velocity of the point in the system, where \[0,0\] is the point not moving initially.
The velocity is in meters per second
Example :

```python
startingvelocity = [
    15,
    2
]
```

The default value is [0,0]

#### `radius`, meters, integer

This parameter is purely graphical, if you want to render different scale bodies or whatnot.

The default value is `5`
> Well actually it is 0, but to avoid any accidental invisible point, any radius of 0 is turned into 5 while rendering.
> This may be changed in the future

#### `color`, RGB triplet, tuple of size 3

This parameter is also graphical and is the color of the point in the GUI
Example :

```python
color = (255, 0, 255)
```

The default value is (255, 255, 255), a white point

#### `historysetting`, boolean

Whether the point's position history is shown.
Any point where historysetting won't have their positions recorded as to improve performance.

The default value is `False`

#### `historylength`, integer

This is how much of the position history will be shown. It is not a time reference, only an array length one.
The time length shown changes with `historyprecision`

A very high value will tank performance, especially if the history of multiple points are shown

The default value is `50`

#### `historycolor`, RGB triplet, tupleof size 3

This parameter is the color of the history line shown.

The default value is `(204, 0, 204)`

#### `historyprecision`

This parameter changes how "fine" the history line looks line. A higher historyprecision makes the history line look
more "jagged", but also improves performance as it reduces the number of positions saved to the history array.

