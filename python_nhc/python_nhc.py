# -*- coding: utf-8 -*-

import json
import logging
import threading
from .nhc_connection import NhcConnection
from .nhc_action import NhcAction

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NhcHub:

    def __init__(self, host, port=8000):
        self._host = host
        self._port = port
        self._actions = self.listActions()
        daemon = threading.Thread(name='daemon', target=self.run)
        daemon.setDaemon(True)
        daemon.start()
        return None

    def run(self):
        connection = NhcConnection(self._host, self._port)
        logger.info(">Connection on {}:{}".format(self._host, self._port))
        connection.send("{\"cmd\": \"startevents\"}")
        while True:
            data = connection.receive()
            if not data:
                break
            elif not data.isspace():
                d = json.loads(data)
                logger.info(">> Data recieved: {}".format(d))
                # Modify status of action when event recieved
                if 'event' in d.keys():
                    d_ev = json.loads(json.dumps(d['data'][0]))
                    actionId = d_ev['id']
                    newVal = d_ev['value1']
                    logger.info(">>new event: id:{} , val:{}".format(
                        actionId, newVal))
                    a = self.getAction(actionId)
                    a.setState(newVal)
        connection.close()
        return None

    def getActions(self):
        return self._actions

    def getAction(self, actionId):
        return self._actions[actionId]

    def getLights(self):
        lights = []
        for a in self.getActions:
            if a.isLight():
                lights.append(a)
        return lights

    def getShutters(self):
        shutters = []
        for a in self.getActions:
            if a.isShutters():
                shutters.append(a)
        return shutters

    def listActions(self):
            actions = {}
            connection = NhcConnection(self._host, self._port)
            data = connection.send("{\"cmd\": \"listactions\"}")
            logger.info(">> Data recieved: {}".format(data))
            data = json.loads(data)
            for a in data['data']:
                actionId = a['id']
                actionName = a['name']
                actionType = a['type']
                actionState = a['value1']
                actions[actionId] = NhcAction(actionId, actionName, actionType, actionState)
                logger.info(">> Action created: {}".format(actions[actionId]))
            return actions

    def listLocations(self):
            connection = NhcConnection(self._host, self._port)
            data = connection.send("{\"cmd\": \"listlocations\"}")
            logger.info(">> Data recieved: {}".format(data))
            s.close()
            return None

    def modifyActionState(self, actionId, newState):
        a = self.getAction(actionId)
        command = a.getNewStateCommand(newState)
        connection = NhcConnection(self._host, self._port)
        data = connection.send(command)
        logger.info(">> Data recieved: {}".format(data))
        return None
