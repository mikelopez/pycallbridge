from amiwrapper import *
# import the settings locally
try:
    import settings
    user = getattr(settings, "AMI_USER")
    pwd = getattr(settings, "AMI_PASS")
    host = getattr(settings, "PBX")
    channel = getattr(settings, "SIP_CHANNEL")
    debug = getattr(settings, "DEBUG", False)
except ImportError:
    user, pwd, host, channel = "", "", "", ""
    debug = True

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
    call_result = ""
    allowed_keys = ['user', 'host', 'pwd', 'channel', 'source', \
                    'extension', 'context', 'priority', 'account' ]

    def __init__(self, **kwargs):
        # overwrite defaults frm any kwargs
        super(AMICallBridge, self).__init__(**kwargs)
        for k, v in kwargs.items():
            if k in self.allowed_keys:
                setattr(self, k, v) 

    def set_channel(self, value):
        """ Set the channel. E.g: sip/provider """
        setattr(self, "channel", value)

    def set_source(self, value):
        """ Set the source phone number 
        E.g: 13059997777
        """
        setattr(self, "source", value)

    def set_extension(self, value):
        """ Set the destination number - the second number that is 
        called and bridged. Example Format: 13059991111 
        """
        setattr(self, "extension", value)

    def set_context(self, value):
        """ Set the context name """
        setattr(self, "context", value)

    def set_priority(self, value):
        """ Set the priority for the destination extension  """
        setattr(self, "priority", value)

    def get_source(self):
        """ Get the source to dial. Prepends channel.
        E.g: returns: sip/test-channel/source_number
        """
        return getattr(self, "source")

    def get_extension(self):
        """ Get the destination, when doing so prepend asterisk required
        fields. Returns extension
        """
        return getattr(self, "extension")

    def get_context(self):
        """ Get the context, when doing so prepend asterisk 
        required fields
        """
        return getattr(self, "context")

    def get_priority(self):
        """ Get the priority for the destination extension """
        return getattr(self, "priority")

    def get_channel(self):
        """ Get the channel. E.g: sip/provider """
        return getattr(self, "channel", "")

    def bridgecalls(self, *args, **kwargs):
        # start the reactor - overwrite kwargs
        for k, v in kwargs.items():
            try:
                setattr(self, k, v)
            except:
                pass
        try:
            self.info_log("pycallbridge - bridgecalls() :: Running reactor")
            self.run_reactor(self.__bridgecalls)
        except Exception, e:
            self.error_log("pycallbridge - bridgecalls() :: Run reactor failed\n%s"%e)
            raise Exception(e)

    def __bridgecalls(self):
        """ First call source number, then bridge in extension """
        return_result = ""
        def on_connect( protocol ):
            """On Login, attempt to originate the call"""
            df = protocol.originate(
                "%s/%s" % (self.get_channel(), self.get_source()), 
                self.get_context(), 
                self.get_extension(), 
                self.get_priority()
            )
            def on_complete( result ):
                self.info_log("pycallbridge - on_complete() :: %s" % result)
                self.call_result = result
                df = protocol.logoff()
                def on_logoff( result ):
                    # stop safely
                    self.info_log("pycallbridge - on_complete() - Stopping reactor")
                    self.stop_reactor()
                return df.addCallbacks( on_logoff, on_logoff )

            def on_failure( reason ):
                self.error_log("pycallbridge - on_failure() :: %s" % reason.getTraceback())
                self.error_log("pycallbridge - on_failure() :: %s" % reason)
                self.error_log("pycallbridge - on_failure() :: Stopping reactor")
                df = protocol.logoff()
                self.stop_reactor()
                return reason.getTraceback()

            df.addErrback( on_failure )
            df.addCallbacks( on_complete, on_complete )
            return df 

        def on_error( reason ):
            """Unable to log in!"""
            self.response = dir(reason)
            print "Authentication Error"
            self.stop_reactor()
            self.error_log(reason)
            self.error_log(reason.getTraceback())

        try:
            df = self.set_session().login(self.host, 5038).addCallbacks(on_connect, on_error)
        except Exception, e:
            return e
        if not self.session:
            self.exception("Failed to set the session")
        if not df:
            self.exception(df)
        return self.call_result



if __name__ == '__main__':
    first_number = raw_input("\n\nEnter the first number to call")
    second_number = raw_input("\n\nEnter the second number to call")

    args = {'host': host, 'user': user, 'pwd': pwd,\
            'channel': channel, 'source': first_number, \
            'extension': second_number}
    cl = AMICallBridge(**args)
    reactor.callWhenRunning(cl.bridgecalls())
    reactor.run()


