# -*- coding: utf-8 -*-

import json
import logging
import threading
from .nhc_connection import NhcConnection
from .nhc_action import NhcAction, NhcLight

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NhcHub:

    def __init__(self, host, port = 8000):
        self._host = str(host)
        self._port = int(port)
        self._actions = self.listActions()
        daemon = threading.Thread(name='daemon', target=self.run)
        daemon.setDaemon(True)
        daemon.start()
        return None

    def run(self):
        connection = NhcConnection(self._host, self._port)
        logger.debug(">Connection on {}:{}".format(self._host, self._port))
        connection.send("{\"cmd\": \"startevents\"}")
        while True:
            data = connection.receive()
            if not data:
                break
            elif not data.isspace():
                d = json.loads(data)
                logger.debug(">> Data recieved: {}".format(d))
                # Modify status of action when event recieved
                if 'event' in d.keys():
                    d_ev = json.loads(json.dumps(d['data'][0]))
                    actionId = d_ev['id']
                    newVal = d_ev['value1']
                    logger.debug(">>new event: id:{} , val:{}".format(
                        actionId, newVal))
                    a = self.getAction(actionId)
                    a.setState(newVal)
        return None

    def getActions(self):
        if self._actions:
            return self._actions
        return None

    def getAction(self, actionId):
        if self._actions[actionId]:
            return self._actions[actionId]
        return None

    def getLights(self):
        lights = []
        for k in self.getActions().keys():
            a = self.getAction(k)
            if a.isLight():
                lights.append(a)
        return lights

    def getCovers(self):
        covers = []
        for k in self.getActions().keys():
            a = self.getAction(k)
            if a.isCover():
                covers.append(a)
        return covers

    def listActions(self):
        actions = {}
        connection = NhcConnection(self._host, self._port)
        data = connection.send("{\"cmd\": \"listactions\"}")
        logger.debug(">> Data recieved: {}".format(data))
        data = json.loads(data)
        for a in data['data']:
            actionId = a['id']
            actionName = a['name']
            actionType = a['type']
            actionState = a['value1']
            if str(actionType) == '1':
                actions[actionId] = NhcLight(self, actionId, actionName, actionType, actionState)
            else:
                actions[actionId] = NhcAction(self, actionId, actionName, actionType, actionState)
            logger.debug(">> Action created: {}".format(actions[actionId]))
        return actions

    def listLocations(self):
        connection = NhcConnection(self._host, self._port)
        data = connection.send("{\"cmd\": \"listlocations\"}")
        logger.debug(">> Data recieved: {}".format(data))
        return None

    def modifyActionState(self, actionId, newState):
        a = self.getAction(actionId)
        command = a.getNewStateCommand(newState)
        connection = NhcConnection(self._host, self._port)
        data = connection.send(command)
        logger.debug(">> Data recieved: {}".format(data))
        return None

    def sendHubCommand(self, command):
        connection = NhcConnection(self._host, self._port)
        data = connection.send(command)
        logger.debug(">> Data recieved: {}".format(data))
        return None
