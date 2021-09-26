class KeysManager:

    def __init__(self) -> None:
        self.dict = {}
        self._isDown = False
        self._isUp = False
        self._isClick = False

    '''
    keyUse: PlayerKeys1 or PlayerKeys2
    '''
    def addKey(self, keyUse):
        self.dict[keyUse] = {}
        self.dict[keyUse]['down'] = False
        self.dict[keyUse]['up'] = False
        self.dict[keyUse]['click'] = False

    def setKeyDown(self, keyUse):
        if not self.dict[keyUse]['down']:
            self.dict[keyUse]['down'] = True
            self.dict[keyUse]['click'] = False
    def setKeyUp(self, keyUse):
        if self.dict[keyUse]['down']:
            self.dict[keyUse]['down'] = False
            self.dict[keyUse]['click'] = True
        
    def isKeyClick(self, keyUse):
        return self.dict[keyUse]['click']
    # is Up and is Down is not usable, please use pygame.mouse instead
    # def isUp():
    #     return not self._isDown
    # def isDown():
    #     return self._isDown

    def update(self):
        for key, value in self.dict.items():
            value['click'] = False