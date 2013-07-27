import sys
import os
from starpy import manager
from termprint import termprint
from unittest import TestCase, TestSuite, TextTestRunner
from twisted.internet import reactor

try:
    import settings
except ImportError:
    sys.exit(1)

from pycallbridge import OriginateCall

class TestCallBridges(TestCase):

    def setUp(self):
        try:
            import settings
        except ImportError:
            self.assertTrue(False)

    def break_row(self):
        """ Print a row separation for logs and stdout """
        termprint("", "\n")
        termprint("INFO", "-".join(["-" for x in range(0, 50)]))
        termprint("", "\n\n")

  
    def test_settings(self):
        """ Test the settings """
        self.assertTrue(getattr(settings, "AMI_USER"))
        self.assertTrue(getattr(settings, "AMI_PASS"))
        self.assertTrue(getattr(settings, "PBX"))
        self.break_row()


    def test_create_connection(self):
        """ Test the connection """
        h, un, pw = getattr(settings, "PBX"), \
                    getattr(settings, "AMI_USER"), \
                    getattr(settings, "AMI_PASS")
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

    def test_call_bridge(self):
        """ Test the call briges """
        h, un, pw = getattr(settings, "PBX"), \
                    getattr(settings, "AMI_USER"), \
                    getattr(settings, "AMI_PASS")
        cl = OriginateCalls()
        


if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestCallBridges("test_settings"))
    suite.addTest(TestCallBridges("test_create_connection"))
    #suite.addTest(TestCallBridges("test_call_bridge"))
    TextTestRunner(verbosity=2).run(suite)


