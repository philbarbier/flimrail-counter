### Flimrail counter system

### Receives signal, decodes bits sent and sends control direction
### to train system

import socket

UDP_LISTEN_IP = "209.141.43.9"
UDP_LISTEN_PORT = 25605

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT))

def control_switcher(command) :
    cs = {
        '01': control_go,
        '03': control_reverse,
    }
    m = cs.get(command, control_null)
    return m()

def control_null() :
    return 'Nothing to do'

def control_go() :
    return 'Train is now on'

def control_reverse() :
    return 'Train is on and in reverse'

def main() :
 
    while True:
        data, addr = sock.recvfrom(1024)
        
        dr = repr(data)
        dr = dr[3:len(dr)-1]

        ### print "Data: ", dr 
        print control_switcher(dr)

if __name__ == '__main__' :
    try :
        main()
        
    except KeyboardInterrupt :
        print "Oooooook bye"
