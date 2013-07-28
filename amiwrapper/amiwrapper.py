from termprint import *
from starpy import manager
from twisted.internet import reactor
import sys, logging
import settings

i, e, w = "INFO", "ERROR", "WARNING"

class AMIWrapper(object):
    """ Base class wrapper file for call originating with starpy """

    user = getattr(settings, "AMI_USER")
    pwd = getattr(settings, "AMI_PASS")
    host = getattr(settings, "PBX")
    command_txt = None
    response = None

    allowed_keys = ['user', 'pwd', 'host', 'command_txt', 'response']
    def __init__(self, **kwargs):
        """ Set the credentials or stop the reactor """
        if not self.host or not self.user or not self.pwd:
            raise Exception("No credentials found")
            self.__stop_reactor()
            sys.exit()

        for k, v in kwargs.items():
            if k in self.allowed_keys:
                setattr(self, k, v)
    
    # privates
    def __stop_reactor(self):
        """ Attempt to stop the reactor so the
        application can terminate.
        """
        try:
            reactor.stop()
        except:
            termprint(e, "Failed to stop reactor")
            pass

    def __run_reactor(self, method):
        """ Start and run the reactor """
        reactor.callWhenRunning(method)
        reactor.run()

    def __exception(self, msg, exit=True):
        """ Print any errors and exit """
        termprint(e, msg)
        self.__stop_reactor()
        sys.exit()

    def __set_session(self):
        self.session = manager.AMIFactory(self.user, self.pwd)
        return self.__get_session()

    def __get_session(self):
        """ Get the session from self.session safely """
        return getattr(self, "session", None)

    def get_command(self):
        """ Get the command to send to AMI (if any) """
        return getattr(self, "command_txt", None)

    def set_command(self, value):
        """ Set the command text to send over AMI """
        setattr(self, "command_txt", value)

    # action methods
    def __command(self, cmd_override=None):
        """ Send a command to Asterisk, or fail """
        if cmd_override:
            self.set_command(cmd_override)
        if not self.get_command():
            self.__exception(e, "No command to send. set class.command = 'command to send'")

        def on_connect(ami):
            # on connect callback
            df = ami.command(self.get_command())

            def on_result(result):
                # do something with the result and exit
                self.response = result
                return ami.logoff()
            def on_error(error):
                # callback when any errors occur
                self.response = error
                self.__exception(error.getTraceback())
            def on_complete(result):
                # when completed, just stop the reactor cause were done
                self.__stop_reactor()

            termprint(w, self.get_command())                
            df.addCallbacks(on_result, on_error)
            df.addCallbacks(on_complete, on_complete)

        def on_error(ami):
            # if any errors with intial login, we call __exception
            self.__exception(ami)

        df = self.__set_session().login(self.host, 5038).addCallbacks(on_connect, on_error)
        if not self.session:
            self.__exception("Failed to set the session")
        if not df:
            self.__exception(df)


    def command(self):
        # start the reactor 
        self.__run_reactor(self.__command)

        



if __name__ == '__main__':
    #manager.log.setLevel(logging.DEBUG)

    # send a command
    cl = AMIWrapper(command="dialplan show from-internal")
    reactor.callWhenRunning(cl.command)
    reactor.run()


