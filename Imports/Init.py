import pygame as pg
import pymunk as pm
import pymunk.pygame_util
import math as mth
import os
import random
from typing import *

from pymunk.vec2d import Vec2d
from Assets.Assets import *
from Constants import *

pg.init()


# ----- Main window --------------------------------

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Tiny football")

space = pm.Space()