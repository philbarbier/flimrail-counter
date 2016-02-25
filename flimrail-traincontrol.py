### Flimrail counter system

### Receives signal, decodes bits sent and sends control direction
### to train system

import socket
import logging
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('config.ini')

UDP_LISTEN_IP = config.get('inet', 'UDP_LISTEN_IP')
UDP_LISTEN_PORT = config.getint('inet', 'UDP_LISTEN_PORT')

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_LISTEN_IP, UDP_LISTEN_PORT))


def control_switcher(command) :
    cs = {
        '01': control_go,
        '03': control_reverse,
    }
    m = cs.get(command, control_off)
    return m()

def control_off() :
    logging.debug("Shutting train off")
    return


def control_go() :
    logging.debug('Train is now on')
    return


def control_reverse() :
    logging.debug('Train is on and in reverse')
    return


def main() :
 
    while True:
        try :
            data, addr = sock.recvfrom(1024)
            
            dr = repr(data)
            dr = dr[3:len(dr)-1]

            ### print "Data: ", dr 
            print control_switcher(dr)
        except IOError:
            logging.debug("Malformed data")

if __name__ == '__main__' :

    try :
        main()
        
    except KeyboardInterrupt :
        logging.debug("Shutting down")
