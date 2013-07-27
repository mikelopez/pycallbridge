from test_base import *
from pycallbridge import OriginateCalls

class TestOriginateCalls(TestAMIBase):
    """ Demonstrate issuing ami commands """
    def __init__(self):
        super(TestOriginateCalls, self).__init__()

    def test_call_bridge(self):
        """ Test the call briges """
        h, un, pw = getattr(settings, "PBX"), \
                    getattr(settings, "AMI_USER"), \
                    getattr(settings, "AMI_PASS")
        cl = OriginateCalls()