from Imports.Init import *

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, vel: tuple):
        # pass in (x,y) in pm.Space <=> (0,0) is bottom left
        super().__init__()
        self.body = pm.Body()
        self.body.position = x,y
        self.body.mass = 1
        self.body.velocity = vel

        self.shape = pm.Circle(self.body, BALL_R)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = COL_BALL
        self.shape.touchedGoal = False

        self.frames = BALL
        self.maxFrames = len(self.frames)
        self.animIndex = 0
        self.animating = False
        self.image = self.frames[0]
        self.ogImage = self.frames[0]


        space.add(self.body, self.shape)

    def update(self):
        # Keep velocity consistent
        if self.body.velocity.length > B_VEL_UPPER_LIMIT:
            self.body.velocity = self.body.velocity.scale_to_length(B_VEL_UPPER_LIMIT)
        elif self.body.velocity.length < B_VEL_LOWER_LIMIT:
            self.body.velocity = 0,0

        # Stop animating if not moving
        if self.body.velocity.length == 0:
            self.animating = False
        else:
            self.animating = True

    def draw(self):
        blitPos = self.body.position[0] - self.shape.radius, self.body.position[1] - self.shape.radius
        
        # fix blitPos slightly, if angle is diagonal
        if 1 < round(self.body.angle) % 10 < 9:
            blitPos = blitPos[0] - 8, blitPos[1] - 8

        if self.animating:
            self.image = self.frames[int(self.animIndex)]
            self.animIndex = self.animIndex + B_ANIM_SPEED * (self.body.velocity.length * mth.log(self.body.velocity.length, 100))
            if self.animIndex >= self.maxFrames - 1:
                self.animIndex = 0

        # rotate ball
        self.body.angle = self.body.velocity.get_angle_degrees_between(Vec2d(1,0))
        self.image = pg.transform.rotozoom(self.frames[int(self.animIndex)], self.body.angle, 1)

        # slow ball down
        self.body.velocity *= B_FRICTION

        # For debug! Draws the Body and Shape of the ball itself in Pymunk
        # pg.draw.circle(screen, RED, self.body.position, self.shape.radius)
        
        
        screen.blit(self.image, blitPos)
