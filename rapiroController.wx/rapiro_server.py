#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import socket
import rapiro
import sys

HOST = None
PORT = 12345
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
       s = socket.socket(af, socktype, proto)
    except socket.error, msg:
       s = None
       continue
    try:
       s.bind(sa)
       s.listen(1)
    except socket.error, msg:
       s.close()
       s = None
       continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    try:
        data = conn.recv(1024)
        print(data)
        t, s, r = rapiro.command(data)
        if not data: break
        conn.send(r)
    except:
        pass
conn.close()
