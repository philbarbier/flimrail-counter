### Flimrail counter system

### Receives signal, decodes bits sent and sends control direction
### to train system
from socket import socket, AF_INET, SOCK_DGRAM
import logging
from ConfigParser import ConfigParser

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

"""
Think of this like a router - a dictionary of available actions
I'm assuming redstone chips will be sending integers as bytes
"""

actions = {
    0 : "noop",
    1 : "forward",
    2 : "reverse",
    3 : "stop",
}


class TrainCtl :


    def __init__(self, *args, **kwargs) :
        self.port = kwargs.get('port')
        self.listen_addr = kwargs.get('listen_addr')
        logging.debug("Listening on %s:%s" % (self.listen_addr, self.port))
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((self.listen_addr, self.port))
        logging.debug("Binding socket")
        self.state = False
        self.rx() # Sets up the socket, dispatches commands


    def rx(self) :

        logging.debug("Starting dispatcher")
        while True :
            data, addr = self.socket.recvfrom(1024)
            try :
                host, port = addr[0], addr[1]
            except:
                logging.error("Invalid host / port")
                return
            logging.debug("Received : '%s' from %s:%s" % (data, host, port))
            # Convert and lookup command to execute
            payload = {
                "host" : host,
                "port" : port,
                "data" : data,
            }
            self.dispatch(payload)

    def dispatch(self, payload) :
        # Convert bytes to ascii integer
        try :
            decode = int(payload.get('data').decode("ascii"))
        except :
            logging.error("Could not decode bytes to ASCII")
            return

        # Map decoded ascii integer to action string for eval in actions list
        action = actions.get(decode)

        if action : # Action was in actions list, try to evaluate it
            action = "my_%s" % action
            try : 
                logging.debug("Attempting to execute '%s' from %s:%s" % (action, payload.get('host'), payload.get('port')))
                func = getattr(self, action)
                return func()
            except :
                logging.error("Could not evaluate '%s' or method does not exist from %s:%s" % (action, payload.get('host'), payload.get('port')))
                return

        # No action was matched but log whatever they sent anyway
        logging.error("'%s' does not map to a valid action from : %s:%s" % (decode, payload.get('host'), payload.get('port')))


    # No Operation - used for debugging or something?
    def my_noop(self, *args, **kwargs) :
        logging.debug("Nothing to do")
        return


    def my_stop(self, *args, **kwargs) :
        logging.debug('Train is stopped')
        self.state = "halt"
        return


    def my_forward(self, *args, **kwargs) :
        logging.debug('Train is on and moving forward')
        self.state = "forward"
        return

    def my_reverse(self, *args, **kwargs) :
        logging.debug('Train is on and in reverse')
        self.state = "reverse"
        return True


def main() :

    config = ConfigParser()
    config.read('config.ini')

    TrainCtl(
        port = config.getint('inet', 'UDP_LISTEN_PORT'),
        listen_addr = config.get('inet', 'UDP_LISTEN_IP')
    )
 

if __name__ == '__main__' :

    try :
        main()
        
    except KeyboardInterrupt :
        logging.debug("Shutting down")
