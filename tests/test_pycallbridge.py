from test_base import *
from amiwrapper import *
sys.path.append("../")
sys.path.append("../pycallbridge")
from pycallbridge import *

try:
    import settings
    host = getattr(settings, "PBX")
    user = getattr(settings, "AMI_USER")
    pwd = getattr(settings, "AMI_PASS")
    channel = getattr(settings, "SIP_CHANNEL")
    test_source = getattr(settings, "TEST_SOURCE_NUMBER")
    test_extension = getattr(settings, "TEST_EXTENSION_NUMBER")
    test_context = getattr(settings, "TEST_CONTEXT", "from-internal")


except ImportError:
    termprint("ERROR", "Not using settings authentication")
    host, user, pwd, channel = "", "", "", ""
    test_source = ""
    test_extension = ""
    test_context = "from-internal"
    settings = False
    termprint("ERROR", "Please set the following variables in local_settings.py")
    termprint("ERROR", "\t- AMI_USER")
    termprint("ERROR", "\t- AMI_PASS")
    termprint("ERROR", "\t- PBX")
    termprint("ERROR", "\t- SIP_CHANNEL")
    termprint("ERROR", "\t- TEST_SOURCE_NUMBER")
    termprint("ERROR", "\t- TEST_SOURCE_NUMBER")
    sys.exit(1)


class TestCallBridge(TestAMIBase):
    """ Test the AMIWrapper class """
    test_source = test_source
    test_extension = test_extension
    test_context = "from-internal"

    def test_bridge_calls_params(self):
        """ Test the bridging of calls with parameters in the
        class instance 
        """
        if not self.test_source:
            self.test_source = raw_input("\n\nEnter the first number to call")
        if not self.test_extension:
            self.test_extension = raw_input("\n\nEnter the second number to call")

        args = {'host': host, 'user': user, 'pwd': pwd,\
                'channel': channel, 'source': self.test_source, \
                'extension': self.test_extension, 'context': self.test_context}
        cl = AMICallBridge(**args)
        self.assertEquals(cl.host, host)
        self.assertEquals(cl.user, user)
        self.assertEquals(cl.pwd, pwd)
        self.assertEquals(cl.channel, channel)
        self.assertEquals(cl.source, self.test_source)
        self.assertEquals(cl.extension, self.test_extension)
        self.assertEquals(cl.context, self.test_context)
        self.assertEquals(cl.get_channel(), channel)
        self.assertEquals(cl.get_source(), self.test_source)
        self.assertEquals(cl.get_extension(), self.test_extension)
        self.assertEquals(cl.get_context(), self.test_context)

        # bridgecalls can overwrite the params too
        result = cl.bridgecalls()
        self.assertEquals(cl.get_channel(), channel)
        self.assertEquals(cl.get_source(), test_source)
        self.assertEquals(cl.get_extension(), test_extension)
        self.assertEquals(cl.get_context(), test_context)
        termprint("INFO", "RESULT:\n%s\n\n" % result)
        termprint("INFO", "RESULT CLASS:\n%s\n\n" % cl.call_result)

        # some kind of response
        if not cl.response:
            termprint("ERROR", "\nNo response, not functioning or incorrect information")
            termprint("WARNING", cl.__dict__)
        else:
            termprint("WARNING", cl.response)


    def test_bridge_calls(self):
        """ Test sending a command to AMI using wrapper.
        It should only allow allowed_keys as kwargs.
        Additionally tests get/set command
        """
        if not self.test_source:
            self.test_source = raw_input("\n\nEnter the first number to call")
        if not self.test_extension:
            self.test_extension = raw_input("\n\nEnter the second number to call")
        
        args = {'host': host, 'user': user, 'pwd': pwd,\
                'channel': channel, 'source': self.test_source, \
                'extension': self.test_extension, 'context': self.test_context}
        #cl = AMICallBridge(host=host, user=user, pwd=pwd)
        cl = AMICallBridge(**args)
        cl.set_channel(channel)
        self.assertEquals(cl.get_channel(), channel)

        cl.set_source(self.test_source)
        self.assertEquals(cl.get_source(), self.test_source)

        cl.set_extension(self.test_extension)
        self.assertEquals(cl.get_extension(), self.test_extension)

        cl.set_context(self.test_context)
        self.assertEquals(cl.get_context(), cl.context)

        if not cl.response:
            termprint("ERROR", "\nNo response, not functioning or incorrect information")
            termprint("WARNING", cl.__dict__)
        else:
            termprint("WARNING", cl.response)


if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestCallBridge("test_bridge_calls_params"))
    suite.addTest(TestCallBridge("test_bridge_calls"))
    TextTestRunner(verbosity=2).run(suite)
