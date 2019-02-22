# -*- coding: utf-8 -*-

class NhcAction:
    actionTypes = {'1': 'lights', '4': 'shutters'}

    def __init__(self, id, name, type, state):
        """NhcAction constructor"""
        self._id = id
        self._name = str(name)
        self._type = str(type)
        self._state = str(state)

    def __repr__(self):
        """Object representation"""
        return "NhcAction {}({}) -> {}".format(
            self._name,
            self._id,
            self._state)

    def setState(self, newState):
        self._state = str(newState)
        return 1

    def getNewStateCommand(self, expectedNewState):
        TCP_Message = '{"cmd":"executeactions","id":"' + str(self._id) + '","value1":"' + str(expectedNewState) + '"}'
        return TCP_Message

    def getState(self):
        return self._state

    def getType(self):
        return self._type

    def isLight(self):
        if self._type == '1':
            return True
        return False

    def isShutter(self):
        if self._type == '4':
            return True
        return False
