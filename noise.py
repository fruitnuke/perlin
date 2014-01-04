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

def linear_interpolate(a, b, x):
    dy = a-b
    if dy == 0:
        return a
    else:
        return (1/(a-b))*x
    

def noise(n):
    a = math.floor(n)
    b = a + 1
#     (n - a) / b - a
    return random.uniform(-1.0, 1.0)
#     return n/15
#     return linear_interpolate(a, b, n-a)
    

sheight = 200
swidth  = 400


if __name__ == '__main__':
    root = tkinter.Tk()
    
#     field = tkinter.PhotoImage(width=400, height=200)
        
#     for y in range(200):
#         for x in range(400):
#             color = '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#             field.put(color, (x, y))
    
    canvas = tkinter.Canvas(root, width=swidth, height=sheight)
    canvas.pack()
#     canvas.create_image(0, 0, image=field, anchor=tkinter.NW)

    xmin = -5 
    xmax = 5
    xstep = swidth  / (xmax - xmin)
    ystep = sheight / (xmax - xmin)
    ymid  = sheight / 2
    xmid  = swidth  / 2
    
    def dot(x, y):
        """x range is -15 to 15, y range is -1 to 1 (-1 is at the bottom of the field)"""
        xx = (swidth / 2 + (x * xstep))
        ya = -y * ystep
        print('ya', ya)
        yy = ymid + (y * 100 * -1)
        print(x, y, xx, yy)
        canvas.create_rectangle(xx-1, yy-1, xx+1, yy+1, outline='#ff0000')

    scale = 10
    def slope(x, y, gradient):
        xx = xmid + (x * xstep)
        yy = ymid + (y * ystep - 1)
        dx = scale
        dy = gradient * scale
        print(xx, yy, dx, dy)
        canvas.create_line(xx-dx, yy-dy, xx+dx, yy+dy, fill='red')

    for x in range(xmin, xmax+1, 1):
        n = noise(x)
#         print(n, y)
        slope(x, 0, n)
        
    root.lift()
    root.mainloop()
#         
    
        