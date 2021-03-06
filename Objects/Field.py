from Init import *

class Wall:
    def __init__(self, pointA, pointB, id, color = None):
        self.body = pm.Body(body_type = pm.Body.STATIC)

        self.shape = pm.Segment(self.body, pointA, pointB, THICKNESS)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = COL_WALL
        self.shape.id = id

        space.add(self.body, self.shape)

    def draw(self):
        # NOTE: Only draw for debugging
        # No need to draw
        #pg.draw.line(screen, BLUE, self.shape.a, self.shape.b, int(self.shape.radius))
        pass


class Goal(pg.sprite.Sprite):
    def __init__(self, pointA, pointB, id: int):
        super().__init__()
        self.body = pm.Body(body_type = pm.Body.STATIC)

        self.shape = pm.Segment(self.body, pointA, pointB, 5)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = COL_GOAL
        #self.shape.sensor = True
        self.shape.id = id

        space.add(self.body, self.shape)

    def draw(self):
        # NOTE: Only draw for debugging
        # No need to draw
        #pg.draw.line(screen, RED, self.shape.a, self.shape.b, int(self.shape.radius))
        pass