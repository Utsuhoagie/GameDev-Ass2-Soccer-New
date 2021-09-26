from Imports.Init import *

class ScoreController:
    def __init__(self):
        self.score_P1 = 0
        self.score_P2 = 0
    
    def draw(self):
        # TODO: Should draw something that looks better
        scoreSurf = FONT.render("Score P1 = " + str(self.score_P1) + "    Score P2 = " + str(self.score_P2), 1, BLUE)
        screen.blit(scoreSurf, (MIDX - scoreSurf.get_width()//2, 20))