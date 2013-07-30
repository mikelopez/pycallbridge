from amiwrapper import *
# import the settings locally
try:
    import settings
    user = getattr(settings, "AMI_USER")
    pwd = getattr(settings, "AMI_PASS")
    host = getattr(settings, "PBX")
    channel = getattr(settings, "SIP_CHANNEL")
except ImportError:
    user, pwd, host, channel = "", "", "", ""

i, e, w = "INFO", "ERROR", "WARNING"

class AMICallBridge(AMIWrapper):
    """ Base class wrapper file for call originating with starpy """
    user = user
    pwd = pwd
    host = host
    channel = channel
    source = ""
    extension = ""
    context = ""
    priority = "1"

    def __init__(self, **kwargs):
        # overwrite defaults frm any kwargs
        super(AMICallBridge, self).__init__(**kwargs)
        for k, v in kwargs.items():
            if k in self.allowed_keys:
                setattr(self, k, v) 

    def set_source(self, value):
        """ Set the source phone number 
        E.g: 13059997777
        """
        setattr(self, "source", value)

    def get_source(self, value):
        """ Get the source to dial. Prepends channel.
        E.g: returns: sip/test-channel/source_number
        """
        return getattr(self, "source")

    def set_extension(self, value):
        """ Set the destination number - the second number that is 
        called and bridged. Example Format: 13059991111 
        """
        setattr(self, "extension", value)
        return value

    def get_extension(self, value):
        """ Get the destination, when doing so prepend asterisk required
        fields. Returns:
        channel, context, extension, priority
        """
        return getattr(self, "extension", value)

    def bridgecalls(self):
        # start the reactor 
        # self.run_reactor(self.__command)
        pass


if __name__ == '__main__':
    first_number = raw_input("\n\nEnter the first number to call")
    second_number = raw_input("\n\nEnter the second number to call")

    args = {'host': host, 'user': user, 'pwd': pwd,\
            'channel': channel, 'source': first_number, \
            'extension': second_number}
    cl = AMICallBridge(**args)
    reactor.callWhenRunning(cl.bridgecalls())
    reactor.run()


