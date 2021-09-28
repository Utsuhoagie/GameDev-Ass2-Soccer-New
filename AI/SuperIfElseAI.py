from Constants import MIDY
from typing import List, Tuple
from AI.IfElseAI import AIState, IfElseAI
from math import inf
from Objects.Ball import Ball
from Objects.Team import Team
import pygame as pg

class SuperIfElseAI(IfElseAI):
    def __init__(self, team: Team, ball: Ball) -> None:
        super().__init__(team, ball)

    def update(self):
        # execute state
        if not self._ball.shape.touchedGoal:
            if self._state == AIState.GO_TO_COLUMN:
                idx = self._team.getCurIdx()
                if idx == self._columnToGo:
                    self._state = AIState.MOVE_PLAYER
                else:
                    if (self._columnToGo < idx):
                        self._team.goTo('left')
                    else:
                        self._team.goTo('right')
            elif self._state == AIState.MOVE_PLAYER:
                group = self._team.getCurrentPlayerGroup()
                direct, speedup = self._findDirectionSpeedUpInGroupNearTheBall(group.sprites())
                
                for player in group.sprites():
                    player.goToFast(direct, speedup)
        else:
            group = self._team.getCurrentPlayerGroup()

            for player in group.sprites():
                player.body.velocity = 0,0


        # behavior
        # go to the column cleareast with the ball
        nearestColumn = self._findNearestColumnNearTheBall()
        if self._columnToGo != nearestColumn:
            self._columnToGo = nearestColumn
            self._state = AIState.GO_TO_COLUMN

    def _findDirectionSpeedUpInGroupNearTheBall(self, group: list[pg.sprite.Sprite]) -> tuple([str, bool]):
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

        useSpeedUp = False
        if deltaY > 50:
            useSpeedUp = True

        # if a goal keeper, does not go outside the goal
        if self._team.getCurIdx() == 3 and (self._ball.body.position[1] > MIDY + 120 or self._ball.body.position[1] < MIDY - 120):
            direction = ""

        return direction, useSpeedUp