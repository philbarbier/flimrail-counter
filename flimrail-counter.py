### Flimrail counter system

### Receives signal, increments value, sends value

import socket

UDP_LISTEN_IP = "209.141.43.9"
UDP_SEND_IP = "198.84.230.106"
UDP_LISTEN_PORT = 25604
UDP_SEND_PORT = 26027 

CTR_FILE = "flimrail1.ctr"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT))

message = 0

f = open(CTR_FILE, 'r+')

message = int(f.read())
print 'Counter is at: ', message
while True:
    f.seek(0)
    data, addr = sock.recvfrom(1024)

    message += 1
    
    print "RX: ", data
    print "TX: ", message
    print "TX-bytes: ", bytes(message)
    
    sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print "Send-result: ", sendsock.sendto(bytes(message), (UDP_SEND_IP, UDP_SEND_PORT)) 
    f.write(str(message))
    print f.tell()
