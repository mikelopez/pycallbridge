from bridge_calls import *
import settings



class CallBridge:
    """ Base class file for call bridging with starpy """

    host = getattr(settings, "AMI_USER")
    user = getattr(settings, "AMI_PASS")
    pwd = getattr(settings, "PBX")
                  
    def __init__(self):
        """ Set the creds """
        if not self.host or not self.user or not self.pwd:
            raise Exception("No credentials found")
            sys.exit()
        self.bridge_call()

    def bridge_call(self):
        """ Bridge the calls """
        manager.log.setLevel(logging.DEBUG)
        logging.basicConfig()
        reactor.callWhenRunning(main)
        reactor.run()


