from Imports.Init import *


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, id: int):
        super().__init__()
        self.body = pm.Body(body_type = pm.Body.KINEMATIC)
        self.body.position = x, y

        self.shape = pm.Circle(self.body, P1_R)
        self.shape.elasticity = 1
        

        if id == 1:
            self.frames = [P1]    #, P1_CHARGE]
            self.shape.collision_type = COL_PLAYER1
        elif id == 2:
            self.frames = [P2]   #, P2_CHARGE]
            self.shape.collision_type = COL_PLAYER2

        self.shape.id = id

        self.image = self.frames[0]
        self.ogImage = self.frames[0]
        self.angle = mth.degrees(self.body.angle)

        self.touchL = False
        self.touchR = False
        self.touchU = False
        self.touchD = False

        self.fast = False
        self.heldFast = False
        self.stamina = MAX_STAMINA

        space.add(self.body, self.shape)

    def update(self):
        # Heal stamina after releasing Space
        if not self.heldFast and not self.fast and self.stamina < MAX_STAMINA:
            self.stamina += HEAL_STAMINA


    def draw(self):
        blitPos = self.body.position[0] - self.image.get_width()//2, self.body.position[1] - self.image.get_height()//2

        screen.blit(self.image, blitPos)