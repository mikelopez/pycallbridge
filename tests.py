from termprint import termprint
from unittest import TestCase, TestSuite, TextTestRunner


class TestCallBridges(TestCase):

    def setUp(self):
        try:
            import settings
        except ImportError:
            self.assertTrue(False)

    def break_row(self):
        """ Print a row separation for logs and stdout """
        termprint("", "\n\n")
        termprint("INFO", "-".join(["-" for x in range(0, 50)]))

  
    def test_settings(self):
        self.assertTrue(getattr(settings, "AMI_USER"))
        self.assertTrue(getattr(settings, "AMI_HOST"))
        self.assertTrue(getattr(settings, "HOST"))



if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestCallBridges("test_settings"))
  
    TextTestRunner(verbosity=2).run(suite)

