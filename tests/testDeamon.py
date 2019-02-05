import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.42.44",8000))
s.send(u"{\"cmd\": \"startevents\"}".encode('utf-8'))
while True:
    #data = s.recv(4096)
    d = json.loads(s.recv(4096))
    if 'event' in d.keys():
        print(">> Data recieved: {}".format(d['event']))
    print(">> Data recieved: {}".format(d['data']))
s.close()
