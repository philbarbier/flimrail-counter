### Flimrail counter system

### Receives signal, decodes bits sent and sends control direction
### to train system

import socket
import binascii

UDP_LISTEN_IP = "209.141.43.9"
UDP_LISTEN_PORT = 25605

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT))

def get_state() :
    return False 

def main() :
 
    try :
            
        state = 0

        do_read = get_state()

        while True:
            f.seek(0)
            data, addr = sock.recvfrom(1024)

            print "Data Length: ", len(data) 
            print "Data-repr: ", repr(data)
            print "Data-stripped: ", data.strip()
            print "Data: ", binascii.b2a_uu(binascii.a2b_uu(data))


if __name__ == '__main__' :
    try :
        main()
        
    except KeyboardInterrupt :
        print "Oooooook bye"
