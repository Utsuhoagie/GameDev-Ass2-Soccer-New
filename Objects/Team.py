from Managers.KeysManager import KeysManager
import pygame as pg
from Constants import *

class Team:
    '''
    firstRow: tien dao
    fourthRow: thu mon
    '''
    def __init__(self, screen, firstRow, secondRow, thirdRow, fourthRow, keyUse) -> None:
        # dictionary of list player
        self.column = []
        self.column.append(firstRow)
        self.column.append(secondRow)
        self.column.append(thirdRow)
        self.column.append(fourthRow)

        self.curColumnTarget = 0
        self.previousColumnTarget = 0
        self.keyUse = keyUse
        self.screen = screen

        self._keyManager = KeysManager()
        self._keyManager.addKey(keyUse.LEFT)
        self._keyManager.addKey(keyUse.RIGHT)

    def update(self, delta=0, time=0):
        self._handleInput()
        for player in self.column[self.curColumnTarget].sprites():
            player.update()
        
    def _handleInput(self):
        keys = pg.key.get_pressed()

        if keys[self.keyUse.LEFT]:
            self._keyManager.setKeyDown(self.keyUse.LEFT)
        else:
            self._keyManager.setKeyUp(self.keyUse.LEFT)

        if keys[self.keyUse.RIGHT]:
            self._keyManager.setKeyDown(self.keyUse.RIGHT)
        else:
            self._keyManager.setKeyUp(self.keyUse.RIGHT)

        if self.keyUse == Player1Keys:
            if self._keyManager.isKeyClick(self.keyUse.LEFT):
                if (self.curColumnTarget < len(self.column)- 1):
                    self.previousColumnTarget = self.curColumnTarget
                    self.curColumnTarget += 1

            if self._keyManager.isKeyClick(self.keyUse.RIGHT):
                if (self.curColumnTarget > 0):
                    self.previousColumnTarget = self.curColumnTarget
                    self.curColumnTarget -= 1
        elif self.keyUse == Player2Keys:
            if self._keyManager.isKeyClick(self.keyUse.LEFT):
                if (self.curColumnTarget > 0):
                    self.previousColumnTarget = self.curColumnTarget
                    self.curColumnTarget -= 1

            if self._keyManager.isKeyClick(self.keyUse.RIGHT):
                if (self.curColumnTarget < len(self.column)- 1):
                    self.previousColumnTarget = self.curColumnTarget
                    self.curColumnTarget += 1

    def update(self):
        self._handleInput()

        for playerInCol in self.column[self.curColumnTarget]:
            playerInCol.update()
        # set zerovelocity before switch to other column
        if self.previousColumnTarget != self.curColumnTarget:
            for playerInCol in self.column[self.previousColumnTarget]:
                playerInCol.setZeroVelocity()
            self.previousColumnTarget = self.curColumnTarget

        self._keyManager.update()

    def draw(self):
        firstPlayerInColumn =  self.column[self.curColumnTarget].sprites()[0].body

        color = LIGHTBLUE if self.keyUse == Player1Keys else ORANGE
        pg.draw.line(self.screen, color, (firstPlayerInColumn.position[0], MENU_HEIGHT), (firstPlayerInColumn.position[0], HEIGHT), 3)

    '''
    FOR AI
    '''
    def getCurIdx(self):
        return self.curColumnTarget

    def goTo(self, direction):
        if direction == 'left':
            if (self.curColumnTarget > 0):
                self.previousColumnTarget = self.curColumnTarget
                self.curColumnTarget -= 1

        elif direction == 'right':
            if (self.curColumnTarget < len(self.column)- 1):
                self.previousColumnTarget = self.curColumnTarget
                self.curColumnTarget += 1

        # set zerovelocity before switch to other column
        if self.previousColumnTarget != self.curColumnTarget:
            for playerInCol in self.column[self.previousColumnTarget]:
                playerInCol.setZeroVelocity()
            self.previousColumnTarget = self.curColumnTarget

    def getCurrentPlayerGroup(self) -> pg.sprite.Group:
        return self.column[self.curColumnTarget]