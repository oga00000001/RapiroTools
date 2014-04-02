#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import  sys,getopt
import  socket
import  threading
import  ipget
import  netaddr
import  rapiro

HOST = None
PORT = 12345
s = None

def keyIn():
    cont = True
    while cont:
        s = raw_input()
        if s == 'x':
            cont = False


def connector():
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
    return(conn, addr)
def receiver(conn):
    while 1:
        try:
            data = conn.recv(1024)
            t, s, r = rapiro.command(data)
            if not data: break
            conn.send(r)
            print(r)
        except:
            pass
    addr = None
    print 'Disconnect'
    conn.close()
    return(addr)

def main():
    addr = None
    cont = True
    while cont:
        try:
            if addr is None:
                conn, addr = connector()
            addr = receiver(conn)
        except:
            cont = False

if __name__ == "__main__":
    try:
        options, args = getopt.getopt(sys.argv[1:],"p:")
    except:
        pass
    else:
        opt_dic = dict(options)
    for key in opt_dic.keys():
        if key == "-p":
            PORT = opt_dic["-p"]
    pi=ipget.ipget()
    print pi
    ipeth0=pi.ipaddr("eth0")
    print("Rapiro command server. port=%s %s\n x:exit program"%(ipeth0,PORT))
    t1 = threading.Thread(target=main)
    t1.setDaemon(True)
    t1.start()
    keyIn()
