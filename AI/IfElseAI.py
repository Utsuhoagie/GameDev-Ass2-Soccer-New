from math import inf
from typing import Tuple
from Objects.Ball import Ball
from Objects.Team import Team
from enum import Enum
import pygame as pg

class AIState(Enum):
    GO_TO_COLUMN = 0
    MOVE_PLAYER = 1

class IfElseAI:
    def __init__(self, team: Team, ball: Ball) -> None:
        self._state = AIState.GO_TO_COLUMN
        self._team = team
        self._ball = ball

        # 0 is the first, 3 is last
        self._columnToGo = 0

    def get_press(self):
        pass

    def update(self):
        # execute state
        if self._state == AIState.GO_TO_COLUMN:
            idx = self._team.getCurIdx()
            if idx == self._columnToGo:
                self._state = AIState.MOVE_PLAYER
            else:
                print(self._columnToGo)
                if (self._columnToGo < idx):
                    self._team.goTo('left')
                else:
                    self._team.goTo('right')
        elif self._state == AIState.MOVE_PLAYER:
            group = self._team.getCurrentPlayerGroup()
            direct = self._findDirectionInGroupNearTheBall(group.sprites())
            
            for player in group.sprites():
                player.goTo(direct)
            

        # behavior
        # go to the column cleareast with the ball
        nearestColumn = self._findNearestColumnNearTheBall()
        if self._columnToGo != nearestColumn:
            self._columnToGo = nearestColumn
            self._state = AIState.GO_TO_COLUMN
        

    def _findDirectionInGroupNearTheBall(self, group: list[pg.sprite.Sprite]) -> str:
        nearestIdx = 0
        direction = ''
        deltaY = inf
        y = self._ball.body.position[1]
        for playerIdx in range(0, len(group)):
            delta = abs(group[playerIdx].body.position[1] - y)
            if delta < deltaY:
                nearestIdx = playerIdx
                deltaY = delta

        if group[nearestIdx].body.position[1] > y:
            direction = 'up'
        else:
            direction = 'down'
        return direction

    def _findNearestColumnNearTheBall(self) -> int:
        for idx in range(0, len(self._team.column)):
            if self._team.column[idx].sprites()[0].body.position[0] > self._ball.body.position[0]:
                return idx
        return 3