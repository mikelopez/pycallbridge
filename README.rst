Readme for pycallbridge
------------------------------

``from pycallbridge import *``


Sample Settings
----------------
Add the following to settings if you are running the tests

.. code-block:: python

    AMI_USER = "admin-user"
    AMI_PASS = "password"
    PBX = "x.x.x.x"

    SIP_CHANNEL = "sip/provider"

    TEST_CONTEXT = "from-internal"    
    TEST_SOURCE_NUMBER = '13051239999'
    TEST_EXTESION_NUMBER = '3051119999'


Sample usage
-------------
You can pass all the required keyword arguments when instantiating the class as shown below, or you can
provide the bare essentials to connect, and later pass them in the method that directly calls the 
call bridging action (See Secondary Usage below)

.. code-block:: python

    from pycallbridge import *

    args = {'host': host, 'user': user, 'pwd': pwd,\
            'channel': channel, 'source': first_number, \
            'extension': second_number, 'context': "from-internal"}
    cl = AMICallBridge(**args)
    cl.bridgecalls()
    

Secondary Usage
---------------
You can also overwrite the channel, extension, source and context parameters when calling bridgecalls() as well.
Note, the source is the number called first, the extension is the second number that is called. The first number
will experience hearing some ringing tones until the other line is answered, the second user experiences no wait


.. code-block:: python

    from pycallbridge import *

    cl = AMICallBridge(host="x.x.x.x", user="admin", pwd="password123")
    cl.bridgecalls(channel="sip/outbound", source="3052229999",\
                   extension="7869999999", context="from-internal")


Response
---------

You can see the response of the call bridge by checking ``cl.response`` variable or running ``cl.get_response()``

