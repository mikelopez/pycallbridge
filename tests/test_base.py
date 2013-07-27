import sys
from starpy import manager
from termprint import termprint
from unittest import TestCase, TestSuite, TextTestRunner
sys.path.append('../')
sys.path.append('../pycallbridge')

try:
    import settings
except ImportError:
    termprint("ERROR", "No settings found")
    sys.exit(1)
from pycallbridge import CallBridge

class TestAMIBase(TestCase):
    """ Base test class for ami functionality that will be used """

    PBX = getattr(settings, "PBX")
    AMI_USER = getattr(settings, "AMI_USER")
    AMI_PASS = getattr(settings, "AMI_PASS")

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
    

    


if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestAMIBase("test_settings"))
    suite.addTest(TestCallBridges("test_call_bridge"))
    TextTestRunner(TestAMIBase=2).run(suite)


