try:
    from local_settings import *
except ImportError:
    print "No settings found! If you do not want settings, create the\
    file and leave empty to disregard this message."
    pass
