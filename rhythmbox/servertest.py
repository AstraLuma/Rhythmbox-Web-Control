import glib
from webctl.server import *

server = Server(listen=('', 8888))
with server:
    ml = glib.MainLoop()
    ml.run()
