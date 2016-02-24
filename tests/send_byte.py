import socket
import os

UDP_IP = "10.0.0.17"
UDP_PORT = 25605

# Sends one random byte (including non-ascii) to the dispatcher
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True :
    msg = raw_input("Enter text to send or (b) for random byte :")
    if msg is 'b' :
        msg = os.urandom(1)
    print "msg:", msg
    print sock.sendto(msg, (UDP_IP, UDP_PORT))
