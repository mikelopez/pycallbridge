from test_base import *


class TestAMICommand():
    """ Demonstrate issuing ami commands """

    def test_ami_command(self):
        """ Test the connection """
        h, un, pw = getattr(settings, "PBX"), \
                    getattr(settings, "AMI_USER"), \
                    getattr(settings, "AMI_PASS")

        def onConnect(ami):
            termprint("WARNING", dir(ami))
            # callbacks for onConnect
            def onResult(result):
                termprint("INFO", result)
                return ami.logoff()
            def onError(reason):
                termprint("ERROR", reason.getTraceback())
                return reason
            def onFinished(result):
                reactor.stop()
            df = ami.command('dialplan show from-internal')
            df.addCallbacks(onResult, onError)
            df.addCallbacks(onFinished, onFinished)
            return df
        session = manager.AMIFactory(un, pw)
        df = session.login(h, 5038).addCallback(onConnect)
        if not df:
            AssertionError(df, exit=True)
        termprint("INFO", df)


if __name__ == '__main__':
    # run with reactor
    cl = TestAMICommand()
    reactor.callWhenRunning(cl.test_ami_command)
    reactor.run()
