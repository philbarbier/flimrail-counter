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

def get_counter_value(f) :
    cv = int(f.read())
    return cv 

def get_state() :
    return True 

def main() :
    
    with open(CTR_FILE, 'r+') as f:
        state = 0

        do_read = get_state()

        message = get_counter_value(f)
        print 'Counter is at: ', message
        while True:
            f.seek(0)
            data, addr = sock.recvfrom(1024)

            state += 1

            if (state % 2) == 0 :
                do_read = True
            
            if do_read :
                message += 1
                
                print "RX: ", data
                print "TX: ", message
                print "TX-bytes: ", bytes(message)
                
                sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print "Send-result: ", sendsock.sendto(bytes(message), (UDP_SEND_IP, UDP_SEND_PORT)) 
                f.write(str(message))
                do_read = False
    ### clean up, clean up like a good wittle boy!
    f.close()

if __name__ == '__main__' :
    try :
        main()
    except KeyboardInterrupt :
        print "Oooooook bye"
