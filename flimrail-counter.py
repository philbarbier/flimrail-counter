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
    cv = f.read()
    if cv == '' : 
        return 0
    return int(cv)

def get_state() :
    return False 

def main() :
 
    try :
        with open(CTR_FILE, 'r+') as f :
            
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
                
                if do_read == True :
                    message += 1
                    tx_message = int(str(message)[::-1])
                    sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    f.write(str(message))

                    print "RX: ", data
                    print "CTR: ", message
                    print "TX: ", tx_message
                    print "TX-bytes: ", bytes(tx_message)
                    print "SR: ", sendsock.sendto(bytes(tx_message), (UDP_SEND_IP, UDP_SEND_PORT)) 

                do_read = False

        ### clean up, clean up like a good wittle boy!
        f.close()

    except IOError :
        open(CTR_FILE, 'w')
        ### let's try that again, shall we?
        main()

if __name__ == '__main__' :
    try :
        main()
        
    except KeyboardInterrupt :
        print "Oooooook bye"
