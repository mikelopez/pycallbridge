from test_base import *
from amiwrapper import *
from pycallbridge.pycallbridge import *

command = "dialplan show from-internal"

class TestAMICommand(TestAMIBase):
    """ Test the AMIWrapper class """

    def test_send_command(self):
        """ Test sending a command to AMI using wrapper.
        It should only allow allowed_keys as kwargs.
        Additionally tests get/set command
        """
        # "command" kwarg is not in allowed keys
        cl = AMICommand(command=command)
        self.assertFalse(cl.get_command() == command)
        # allowed key
        cl = AMICommand(command_txt=command)
        self.assertTrue(cl.get_command() == command)

        # allowed kwarg to specify the command to send
        cl = AMICommand()
        cl.set_command(command)
        self.assertTrue(cl.get_command() == command)

        termprint("INFO", "Running the command on Asterisk...")
        cl.command()
        self.assertTrue(cl.response)
        termprint("INFO", "Response: \n%s" % cl.response)

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestAMICommand("test_send_command"))
    TextTestRunner(verbosity=2).run(suite)
