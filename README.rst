Readme for pycallbridge
------------------------------

``from pycallbridge import *``


Sample Settings
----------------
Add the following to settings if you are running tests


.. code-block:: python

	AMI_USER = "admin-user"
	AMI_PASS = "password"
	PBX = "x.x.x.x"

	SIP_CHANNEL = "sip/provider"

	TEST_SOURCE_NUMBER = '13051239999'
	TEST_EXTESION_NUMBER = '3051119999'


Sample usage
-------------

.. code-block:: python

    from pycallbridge import *

    args = {'host': host, 'user': user, 'pwd': pwd,\
            'channel': channel, 'source': first_number, \
            'extension': second_number}
    cl = AMICallBridge(**args)
    cl.bridgecalls()
    

Secondary Usage
---------------
You can also overwrite the channel, extension, source and context parameters when calling bridgecalls() as well.

.. code-block:: python

    from pycallbridge import *

	cl = AMICallBridge(host="x.x.x.x", user="admin", pwd="password123")
	cl.bridgecalls(channel="sip/outbound", source="3052229999",\
				  extension="7869999999", context="from-internal")



