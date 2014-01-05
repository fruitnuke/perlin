'''Investigations in implementing Perlin noise.

Resources
---------

Perlin noise:  http://freespace.virgin.net/hugo.elias/models/m_perlin.htm
Interpolation: http://paulbourke.net/miscellaneous/interpolation
'''

import unittest
import math
import tkinter
import random


class NoiseTests(unittest.TestCase):

    def test_range(self):
        x = noise(0.5)
        self.assertIsInstance(x, float)
        self.assertTrue(x >= -1.0 and x <= 1.0)

    def test_consistency(self):
        self.assertEqual(noise(0.25), noise(0.25))

    def test_linear_interpolation(self):
        self.assertAlmostEqual(linear_interpolate(1, 2, 0.1), 1.1)
        self.assertAlmostEqual(linear_interpolate(1, 3, 0.1), 1.2)
        self.assertAlmostEqual(linear_interpolate(2, 1, 0.1), 1.9)
        self.assertAlmostEqual(linear_interpolate(1, 2, 0.0), 1.0)
        self.assertAlmostEqual(linear_interpolate(1, 2, 1.0), 2.0)
        self.assertAlmostEqual(linear_interpolate(-1, -2, 0.5), -1.5)
        self.assertAlmostEqual(linear_interpolate(1, -1, 0.5), 0.0)


def linear_interpolate(a, b, dx):
    """Do a linear interpolation between a and b by dx; assumes 0.0 <= dx <= 1.0."""
    return a + (b - a) * dx


def cubic_interpolate(a, b, c, d, dx):
    p = (d - c) - (a - b)
    q = (a - b) - p
    r = c - a
    return (p * math.pow(dx, 3)) + (q * math.pow(dx, 2)) + (r * dx) + b


# need to go to 13 numbers so we have points available to do cubic interpolation between points 0 to 10.
_random = [random.uniform(-1.0, 1.0) for _ in range(14)]
_random_offset = 1
def random_n(n):
    """For the noise function I need a function that maps integers in the local space to pseudo-random numbers. The
    python random module only provides generator like functions, they don't do a mapping like this that can be called
    repeatedly. I could write a simple pseudo-random number implementation, but for now just create a one-off mapping
    for a fixed range of the 1d local space."""
    return _random[n + _random_offset]


def noise(x):
    """A first approximation of perlin noise; do a linear interpolation between pseudo-random numbers at given intervals.

    x is a 1d coordinate in local space, returns a float that represents the noise value at that point.
    """
    a  = math.floor(x)
    dx = x - a
    return cubic_interpolate(random_n(a-1), random_n(a), random_n(a+1), random_n(a+2), dx)


if __name__ == '__main__':
    sheight = 200
    swidth  = 400
    offset  = 10
    xmin  = 0
    xmax  = 10
    xstep = swidth  / (xmax - xmin)
    ystep = sheight / (xmax - xmin)
    ymid  = sheight / 2
    axis_font = ('Verdana', 10)

    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=swidth + (offset*2), height=sheight)
    canvas.pack()

    def axis():
        """Draw the axis of the local 1d coord system."""
        canvas.create_line(offset, ymid, offset+swidth, ymid, fill='gray')
        labels_at = (0, 5, 10)
        for n in range(xmin, xmax+1):
            x = offset + (n * xstep)
            canvas.create_line(x, ymid-3, x, ymid, fill='gray')
            if n in labels_at:
                canvas.create_text(x, ymid+5, text=str(n), anchor=tkinter.N, fill='gray', font=axis_font)

    def point(x, y):
        """draw a graphic mark on the canvas at x, y in the local coord system."""
        xx = offset + (x * xstep)
        yy = ymid - (ymid * y)
        print(x, y, xx, yy)
        canvas.create_rectangle(xx-2, yy-2, xx+2, yy+2, outline='red')

    scale = 10
    def slope(x, y, gradient):
        """draw a line representing the gradient at x, y in the local coord system."""
        xx = (x * xstep)
        yy = ymid + (y * ystep - 1)
        dx = scale
        dy = gradient * scale
        canvas.create_line(xx-dx, yy-dy, xx+dx, yy+dy, fill='red')

    axis()

    # highlight the known pseudo-random points
    for n in range(xmin, xmax + 1):
        point(n, noise(n))

    # draw the noise octave, interpolating between the known random points.
    points = []
    for x in range(0, swidth + 1):
        lx = x / 40
        sx = offset + x
        sy = ymid - round(noise(lx), 7) * ymid
        points.append((sx, sy))
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        canvas.create_line(x1, y1, x2, y2)

    root.title('1d perlin noise')
    root.lift()
    root.mainloop()
