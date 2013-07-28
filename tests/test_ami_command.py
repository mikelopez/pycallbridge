"""
Test AMI commands using strictly starpy and reactor

"""
from test_base import *
e, w, i = "ERROR", "WARNING", "INFO"

class TestAMICommand():
    """ Demonstrate issuing ami commands """
    response = ""
    def test_ami_command(self):
        """ Test the connection """
        h, un, pw = getattr(settings, "PBX"), \
                    getattr(settings, "AMI_USER"), \
                    getattr(settings, "AMI_PASS")

        def onConnect(ami):
            termprint(w, "Connect response\n%s" % dir(ami))
            def onResult(result):
                termprint(i, "Result: %s" % result)
                self.response = result
                return ami.logoff()
            def onError(reason):
                termprint(e, reason.getTraceback())
                reactor.stop()
                return reason
            def onFinished(result):
                reactor.stop()
            dfc = ami.command('dialplan show from-internal')
            dfc.addCallbacks(onResult, onError)
            dfc.addCallbacks(onFinished, onFinished)
            return dfc
            
        def onError(ami):
            termprint(e, dir(ami))
            termprint(e, "Stopping Reactor")
            value = ami.getErrorMessage()
            self.response = ami.value.message
            termprint(e, "errors = %s" % value)
            reactor.stop()

        session = manager.AMIFactory(un, pw)
        df = session.login(h, 5038).addCallbacks(onConnect, onError)
        

        termprint(i, "Login response: \n%s" % dir(df))


if __name__ == '__main__':
    # run with reactor
    cl = TestAMICommand()
    reactor.callWhenRunning(cl.test_ami_command)
    reactor.run()
    termprint(i, "response = %s" % cl.response)
