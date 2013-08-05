"""Example script to generate a call to connect a remote channel to an IVR"""
import sys
import logging
from termprint import *
from starpy import manager
from twisted.internet import reactor
from random import randint

sys.path.append('../')
sys.path.append('../pycallbridge')

import settings as s
test_source = getattr(s, "TEST_SOURCE_NUMBER", "7864445555")
test_exten = getattr(s, "TEST_EXTENSION_NUMBER", "7864445555")
test_context = getattr(s, "TEST_CONTEXT", "from-internal")


def main(channel='sip/kinetic/%s' % (test_source), connectTo=('from-internal','%s' % (test_exten),'1')):

    f = manager.AMIFactory(getattr(s, "AMI_USER"), getattr(s, "AMI_PASS"))
    df = f.login(getattr(s, "PBX"))

    def onLogin( protocol ):
        """On Login, attempt to originate the call"""
        acctid = "XXXX%s" % str(randint(11111,999999))
        context, extension, priority = connectTo
        df = protocol.originate(
            channel, context, extension, priority, callerid="ABC123XY456", account=acctid
        )
        def onFinished( result ):
            termprint("INFO", "FINISHED CALL \n\t%s" % result)
            termprint("ERROR", dir(result))
            df = protocol.logoff()
            def onLogoff( result ):
                reactor.stop()
            return df.addCallbacks( onLogoff, onLogoff )
        def onFailure( reason ):
            print reason.getTraceback()
            return reason 
        df.addErrback( onFailure )
        df.addCallbacks( onFinished, onFinished )
        return df 

    def onFailure( reason ):
        """Unable to log in!"""
        print reason.getTraceback()
        reactor.stop()

    df.addCallbacks( onLogin, onFailure )
    return df



if __name__ == '__main__':
    manager.log.setLevel(logging.DEBUG)
    reactor.callWhenRunning(main)
    reactor.run()
