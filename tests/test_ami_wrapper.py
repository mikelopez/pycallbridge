from test_base import *
from amiwrapper import AMIWrapper

class TestAMIWrapper(TestAMIBase):
    """ Test the AMIWrapper class """
    def test_

    def test_send_command(self):
        """ Test sending a command to AMI using wrapper.
        It should only allow allowed_keys as kwargs.
        """
        # not allowed kwarg command
        cl = AMIWrapper(command="dialplan show from-internal")
        self.assertFalse(cl.get_command() == "dialplan show from-internal")
        # allowed kwarg to specify the command to send
        cl = AMIWrapper()
        cl.set_command("dialplan show from-internal")
        self.assertTrue(cl.get_command() == "dialplan show from-internal")
        
        termprint("INFO", "Running command...")
        cl.command()
        self.assertTrue(cl.response)
        termprint("INFO", "Response: \n%s" % cl.response)

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestAMIWrapper("test_send_command"))
    TextTestRunner(verbosity=2).run(suite)
