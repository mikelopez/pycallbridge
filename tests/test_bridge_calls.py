"""Example script to generate a call to connect a remote channel to an IVR"""
from termprint import *
from starpy import manager
from twisted.internet import reactor
import sys, logging

def main(**kwargs):
    #  channel = 'sip/20035@aci.on.ca', connectTo=('outgoing','s','1') 
    for k in ['channel', 'connect_to', 'user', 'password', 'host']:
        if not kwargs.get(k):
            termprint("ERROR", "Required kwarg %s not present" % k)
            
    f = manager.AMIFactory(kwargs.get('user'), kwargs.get('passwd'))
    df = f.login(kwargs.get('host'))

    def onLogin( protocol ):
        """On Login, attempt to originate the call"""
        context, extension, priority = kwargs.get('connect_to')
        df = protocol.originate(
            kwargs.get('channel'),
            context,extension,priority,
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

