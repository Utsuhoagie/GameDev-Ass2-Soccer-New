from Init import *

class ScoreController:
    def __init__(self):
        self.score_P1 = 0
        self.score_P2 = 0

    def reset(self):
        self.score_P1 = 0
        self.score_P2 = 0
    
    def draw(self):
        # TODO: Should draw something that looks better
        score1Surf = FONT.render("Score P1 = " + str(self.score_P1), 1, LIGHTBLUE)
        screen.blit(score1Surf, (40, 20))

        score2Surf = FONT.render("Score P2 = " + str(self.score_P2), 1, ORANGE)
        screen.blit(score2Surf, (WIDTH - 40 - score1Surf.get_width(), 20))