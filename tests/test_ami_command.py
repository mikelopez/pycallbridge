from test_base import *

class TestAMICommand(TestAMIBase):
    """ Demonstrate issuing ami commands """
    def __init__(self):
        super(TestAMICommand, self).__init__()

    def test_ami_command(self):
        """ Test the connection """
        h, un, pw = getattr(self, "PBX"), \
                    getattr(self, "AMI_USER"), \
                    getattr(self, "AMI_PASS")

        def onConnect( ami ):
            def onResult( result ):
                print 'Result', result
                return ami.logoff()
            def onError( reason ):
                print reason.getTraceback()
                return reason
            def onFinished( result ):
                reactor.stop()
            df = ami.command( 'dialplan show from-internal' )
            df.addCallbacks( onResult, onError )
            df.addCallbacks( onFinished, onFinished )
            return df
        session = manager.AMIFactory(un, pw)
        return session.login(h, 5038).addCallback(onConnect)


if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestAMICommand("test_ami_command"))
    TextTestRunner(verbosity=2).run(suite)
