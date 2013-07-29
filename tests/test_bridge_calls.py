"""Example script to generate a call to connect a remote channel to an IVR"""
import sys
import logging
from termprint import *
from starpy import manager
from twisted.internet import reactor


sys.path.append('../')
sys.path.append('../pycallbridge')
import settings as s


def main(channel = 'sip/kinetic/17863789504', connectTo=('from-internal','17864706212','1')):

    f = manager.AMIFactory(getattr(s, "AMI_USER"), getattr(s, "AMI_PASS"))
    df = f.login(getattr(s, "PBX"))

    def onLogin( protocol ):
        """On Login, attempt to originate the call"""
        context, extension, priority = connectTo
        df = protocol.originate(
            channel,
            context, extension, priority,
        )
        def onFinished( result ):
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
