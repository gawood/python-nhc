import python_nhc as nhc
import logging
import time

logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger.info("> nhc Daemon")
# threading.current_thread()
nhcHub =nhc.NhcHub("192.168.42.44",8000)

# worker = threading.Thread(target=nhcHub.run())
# worker.start()
# worker.setDaemon(True)
logger.info(">> Test: {}".format(nhcHub.getShutters()))
# time.sleep(30)
# logger.info(">> Test: {}".format(nhcHub.getAction(73)))

# print(nhcHub.getAction(14).getState())
# nhcHub.modifyActionState(14,0)
# time.sleep(5)
# print nhcHub.getAction(14).getState()
# nhcHub.modifyActionState(14,100)
# time.sleep(1)
# print nhcHub.getAction(14).getState()
