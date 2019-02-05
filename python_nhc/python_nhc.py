import sys
import time
import logging
import threading
import socket
import json
from .nhcAction import NhcAction

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NhcHub:

    def __init__(self, host, port=8000):
        self.host = host
        self.port = port
        self.actions = self.listActions()
        daemon = threading.Thread(name='daemon', target=self.run)
        daemon.setDaemon(True)
        daemon.start()
        return None

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        logger.info(">Connection on {}:{}".format(self.host, self.port))
        s.send(u"{\"cmd\": \"startevents\"}".encode('utf-8'))
        while True:
            data = s.recv(4096)
            d = json.loads(data)
            logger.info(">> Data recieved: {}".format(d))
            if 'event' in d.keys():
                d_ev = json.loads(json.dumps(d['data'][0]))
                actionId = d_ev['id']
                newVal = d_ev['value1']
                logger.info(">>new event: id:{} , val:{}".format(
                    actionId, newVal))
                a = self.getAction(actionId)
                a.setState(newVal)
        s.close()
        return None

    def getActions(self):
        return self.actions

    def getAction(self, actionId):
        return self.actions[actionId]

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
            output = ""
            actions = {}
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.send(u"{\"cmd\": \"listactions\"}".encode('utf-8'))
            while True:
                d = s.recv(2)
                if len(d) < 2:
                    #logger.info(">> Data recieved: {}".format(output))
                    s.close()
                    break
                output = output + "{}".format(d)
            s.close()
            try:
                output = output.decode('ascii', 'ignore')
            except AttributeError:
                pass
            logger.info(">> Data recieved: {}".format(output))
            output = json.loads(output)
            for a in output['data']:
                actionId = a['id']
                actionName = a['name']
                actionType = a['type']
                actionState = a['value1']
                actions[actionId] = NhcAction(actionId, actionName, actionType, actionState)
                logger.info(">> Action created: {}".format(actions[actionId]))
            return actions

    def listLocations(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            logger.info(">Connection on {}:{}".format(self.host, self.port))
            s.send(u"{\"cmd\": \"listlocations\"}".encode('utf-8'))
            d = json.loads(s.recv(4096))
            logger.info(">> Data recieved: {}".format(d))
            s.close()
            return None

    def modifyActionState(self, actionId, newState):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        logger.info(">Connection on {}:{}".format(self.host, self.port))
        a = self.getAction(actionId)
        command = a.getNewStateCommand(newState)
        s.send(command.encode('utf-8'))
        d = json.loads(s.recv(4096))
        logger.info(">> Data recieved: {}".format(d))
        s.close()
        return None


# def main(argv):
#     logger.info("> nhc Daemon")
#     threading.current_thread()
#     nhcHub = NhcHub("192.168.12.4",8000)
#     print('pwet')
#     # worker = threading.Thread(target=nhcHub.run())
#     # worker.start()
#     # worker.setDaemon(True)
#     logger.info(">> Test: {}".format(nhcHub.getAction(45)))
#     time.sleep(30)
#     logger.info(">> Test: {}".format(nhcHub.getAction(73)))
#
#
# if __name__ == "__main__":
#     logFile = logging.FileHandler('out.log')
#     logFile.setLevel(logging.INFO)
#     logger.addHandler(logFile)
#     ch = logging.StreamHandler()
#     ch.setLevel(logging.DEBUG)
#     logger.addHandler(ch)
#     main(sys.argv[1:])
