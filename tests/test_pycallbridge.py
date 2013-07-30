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

except ImportError:
    host, user, pwd, channel = "", "", "", ""
    settings = False
    termprint("ERROR", "Please set the following variables in local_settings.py")
    termprint("ERROR", "\t- AMI_USER")
    termprint("ERROR", "\t- AMI_PASS")
    termprint("ERROR", "\t- PBX")
    termprint("ERROR", "\t- SIP_CHANNEL")
    sys.exit(1)


class TestCallBridge(TestAMIBase):
    """ Test the AMIWrapper class """
    def test_bridge_calls_params(self):
        """ Test the bridging of calls with parameters in the
        class instance 
        """
        first_number = raw_input("\n\nEnter the first number to call")
        second_number = raw_input("\n\nEnter the second number to call")

        args = {'host': host, 'user': user, 'pwd': pwd,\
                'channel': channel, 'source': first_number, \
                'extension': second_number}
        cl = AMICallBridge(**args)
        cl.bridgecalls()
        # some kind of response
        self.assertTrue(cl.response)
        termprint("WARNING", cl.response)


    def test_bridge_calls(self):
        """ Test sending a command to AMI using wrapper.
        It should only allow allowed_keys as kwargs.
        Additionally tests get/set command
        """
        first_number = raw_input("\n\nEnter the first number to call")
        second_number = raw_input("\n\nEnter the second number to call")
        
        cl = AMICallBridge(host=host, user=user, pwd=pwd)
        cl.set_channel(channel)
        self.assertEquals(cl.get_channel(), channel)

        cl.set_source(first_number)
        self.assertEquals(cl.get_source(), first_number)

        cl.set_destination(second_number)
        self.assertEquals(cl.get_destination(), second_number)


if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestCallBridge("test_bridge_calls"))
    TextTestRunner(verbosity=2).run(suite)
