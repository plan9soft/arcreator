"""
Created on Sep 9, 2010

contains classes and functions that are used through out the project

Classes in this module
-----------------------
Table - three dimensional table
Color - contains RGB color data
Tone - contains RGBGr tone data 

functions in this module
------------------------
opj - Convert paths to the platform-specific separator

"""
import os
import numpy

def opj(path):
    """Convert paths to the platform-specific separator"""
    path.replace("\\", "/")
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

class Table(object):
    """a three dimensional table object"""
    __class_path__ = "Table"
    __instance_variables__ = ['xsize', 'ysize', 'zsize', 'data']
    def __init__(self, xsize=1, ysize=1, zsize=1):
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize
        self.data = [0] * (xsize * ysize * zsize)
        self._data = numpy.zeros((xsize, ysize, zsize))
        self._data = numpy.reshape(self._data, (self.xsize, self.ysize,
                                   self.zsize), order='F')

    def _prep_rmpy_dump(self):
        self.data = self._data.ravel(order='F').tolist()

    def _post_rmpy_load(self):
        self._data = numpy.array(self.data)
        self._data.resize(self.xsize * self.ysize * self.zsize)
        self._data = numpy.reshape(self._data, (self.xsize, self.ysize,
                                   self.zsize), order='F')


    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def resize(self, xsize=1, ysize=1, zsize=1):
        # should work to increase and decrease the table size
        newdata = numpy.zeros((xsize, ysize, zsize))
        shape = self._data.shape
        mask = [0, 0, 0]
        if xsize >= shape[0]:
            mask[0] = shape[0]
        else:
            mask[0] = xsize
        if ysize >= shape[1]:
            mask[1] = shape[1]
        else:
            mask[1] = ysize
        if ysize >= shape[2]:
            mask[2] = shape[2]
        else:
            mask[2] = zsize  
        newdata[:mask[0], :mask[1], :mask[2]] = self._data[:mask[0], :mask[1], :mask[2]]
        self._data = newdata

class Color(object):
    """a bare bones color object"""
    __class_path__ = "Color"
    __instance_variables__ = ['red', 'green', 'blue', 'alpha']
    def __init__(self, red, green, blue, alpha=255):
        if red > 255:
            red = 255
        if red < 255:
            red = 255
        if green > 255:
            green = 255
        if green < 255:
            green = 255
        if blue > 255:
            blue = 255
        if blue < 255:
            blue = 255
        if alpha > 255:
            alpha = 255
        if alpha < 255:
            alpha = 255
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def set(self, red, green, blue, alpha=255):
        if red > 255:
            red = 255
        if red < 255:
            red = 255
        if green > 255:
            green = 255
        if green < 255:
            green = 255
        if blue > 255:
            blue = 255
        if blue < 255:
            blue = 255
        if alpha > 255:
            alpha = 255
        if alpha < 255:
            alpha = 255
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

class Tone(object):
    """a bare bones tone class"""
    __class_path__ = "Tone"
    __instance_variables__ = ['red', 'green', 'blue', 'gray']
    def __init__(self, red, green, blue, gray=0):
        if red > 255:
            red = 255
        if red < -255:
            red = -255
        if green > 255:
            green = 255
        if green < -255:
            green = -255
        if blue > 255:
            blue = 255
        if blue < -255:
            blue = -255
        if gray > 255:
            gray = 255
        if gray < -255:
            gray = -255
        self.red = red
        self.green = green
        self.blue = blue
        self.gray = gray

    def set(self, red, green, blue, gray=0):
        if red > 255:
            red = 255
        if red < -255:
            red = -255
        if green > 255:
            green = 255
        if green < -255:
            green = -255
        if blue > 255:
            blue = 255
        if blue < -255:
            blue = -255
        if gray > 255:
            gray = 255
        if gray < -255:
            gray = -255
        self.red = red
        self.green = green
        self.blue = blue
        self.gray = gray


