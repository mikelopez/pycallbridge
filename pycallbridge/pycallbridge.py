from bridge_calls import *
import settings

class OriginateCalls:
    """ Base class wrapper file for call originating with starpy """

    user = getattr(settings, "AMI_USER")
    pwd = getattr(settings, "AMI_PASS")
    host = getattr(settings, "PBX")
                  
    def __init__(self):
        """ Set the creds """
        if not self.host or not self.user or not self.pwd:
            raise Exception("No credentials found")
            sys.exit()
    
    def __session(self):
        return manager.AMIFactory(self.user, self.pwd)

    def command(self, cmd):
        """ Send a command to Asterisk """
        pass


if __name__ == '__main__':
    #manager.log.setLevel(logging.DEBUG)
    #logging.basicConfig()
    reactor.callWhenRunning(main)
    reactor.run()


