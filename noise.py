'''
Created on Jan 1, 2014

@author: dan
'''

import unittest
import math
import tkinter
import random


class NoiseTests(unittest.TestCase):
    
    def test_foo(self):
        x = noise(0.5)
        self.assertIsInstance(x, float)
        self.assertTrue(x >= -1.0 and x <= 1.0)


def linear_interpolate(a, b, dx):
    """Do a linear interpolation between a and b by dx.
    
    Assumes 0.0 <= dx <= 1.0"""
    res = a + (b - a) * dx
    print ('interp', a, b, dx, res)
    return res 


# need to go to 11 numbers so that we can interpolate around 10
_random = [random.uniform(-1.0, 1.0) for _ in range(12)] 
def random_n(n):
    """For the noise function I need a function that maps integers in the local space to pseudo-random numbers. The 
    python random module only provides generator like functions, they don't do a mapping like this that can be called
    repeatedly. I could write a simple pseudo-random number implementation, but for now just create a one-off mapping
    for a fixed range of the 1d local space."""
    return _random[n]


def noise(x):
    """A first approximation of perlin noise; do a linear interpolation between pseudo-random numbers at given intervals.
    
    x is a 1d coordinate in local space, returns a float that represents the noise value at that point.
    """
    a  = math.floor(x)
    b  = a + 1 
    dx = x - a
    print('noise', x, a, b, dx, random_n(a), random_n(b))    
    return linear_interpolate(random_n(a), random_n(b), dx)
    

if __name__ == '__main__':
    sheight = 200
    swidth  = 400
    offset  = 5
    xmin = 0 
    xmax = 10
    xstep = swidth  / (xmax - xmin)
    ystep = sheight / (xmax - xmin)
    ymid  = sheight / 2
    
#     field = tkinter.PhotoImage(width=400, height=200)        
#     for y in range(200):
#         for x in range(400):
#             color = '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#             field.put(color, (x, y))
#     canvas.create_image(0, 0, image=field, anchor=tkinter.NW)
    
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=swidth + offset, height=sheight)
    canvas.pack()
    
    def mark(x, y):
        """draw a graphic mark on the canvas at x, y in the local coord system.""" 
        xx = offset + (x * xstep)
        yy = ymid + (y * ystep * -1)
        print(x, y, xx, yy)
        canvas.create_rectangle(xx-1, yy-1, xx+1, yy+1, outline='#ff0000')

    scale = 10
    def slope(x, y, gradient):
        """draw a line representing the gradient at x, y in the local coord system."""
        xx = (x * xstep)
        yy = ymid + (y * ystep - 1)
        dx = scale
        dy = gradient * scale
        canvas.create_line(xx-dx, yy-dy, xx+dx, yy+dy, fill='red')

    for x in range(xmin, xmax+1):
        mark(x, 0)
        
    for x in range(0, swidth-1):
        lx = x / 40
        sx = offset + x 
        ly = noise(lx)
        sy = int(ymid + (ly * ymid - 1))
        print('xx', lx, ly, sx, sy)
        canvas.create_rectangle(sx, sy, sx, sy, fill='black')
        
    root.lift()
    root.mainloop()
    
        