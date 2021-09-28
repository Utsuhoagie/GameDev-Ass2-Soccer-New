from Init import *

class ScoreController:
    def __init__(self):
        self.score_P1 = 0
        self.score_P2 = 0
        self.win = 0
        self.timer = 0

    def reset(self):
        self.score_P1 = 0
        self.score_P2 = 0

    def update(self):
        if self.score_P1 == WIN_COND and self.win == 0:
            self.win = 1
            self.timer = 90
        elif self.score_P2 == WIN_COND and self.win == 0:
            self.win = 2
            self.timer = 90

        self.timer -= 1
        if self.timer == 0:
            pg.event.post(pg.event.Event(EVENT_MENU))

        

    def draw(self):
        # TODO: Should draw something that looks better
        score1Surf = FONT.render("Score P1 = " + str(self.score_P1), 1, LIGHTBLUE)
        screen.blit(score1Surf, (20, 45))

        score2Surf = FONT.render("Score P2 = " + str(self.score_P2), 1, ORANGE)
        screen.blit(score2Surf, (WIDTH - 20 - score1Surf.get_width(), 45))

        winCondSurf = WIN_COND_FONT.render("First to " + str(WIN_COND) + " wins!", 1, BLACK)
        bgWinCond = winCondSurf.get_rect()
        bgWinCond.width += 15
        bgWinCond.height += 10
        bgWinCond.center = MIDX, 20
        pg.draw.rect(screen, WHITE, bgWinCond)
        screen.blit(winCondSurf, (MIDX - winCondSurf.get_width()//2, 12))


        if self.win != 0:
            txt = "Player 1 wins!" if self.win == 1 else "Player 2 wins!"
            color = LIGHTBLUE if self.win == 1 else ORANGE

            txtSurf = FONT.render(txt, 1, color)
            bgRect = txtSurf.get_rect()
            bgRect.width += 30
            bgRect.height += 30
            bgRect.center = MIDX, MIDY

            bgBorder = txtSurf.get_rect()
            bgBorder.width += 50
            bgBorder.height += 50
            bgBorder.center = MIDX, MIDY

            pg.draw.rect(screen, color, bgBorder)
            pg.draw.rect(screen, BLACK, bgRect)

            screen.blit(txtSurf, (bgRect.center[0] - txtSurf.get_width()//2, bgRect.center[1] - txtSurf.get_height()//2))