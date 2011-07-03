# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
Basic JSON webserver for Rhythmbox
"""
from __future__ import division, absolute_import, with_statement
import rb
import gobject, gtk, gio
from .server import Server

__all__ = 'WebCtl',

class WebCtl(rb.Plugin):
	def __init__(self):
		super(WebCtl, self).__init__()
	
	def activate(self, shell):
		self.shell = shell
		# Load config file
		
		# Start the webserver
		self.server = Server(rbshell=shell, **self.config)
		self.server.__enter__() # Start the server
	
	def deactivate(self, shell):
		self.server.__exit__(None, None, None) # Make sure the server cleans up, need it to remove the reference to shell
		del self.server
		del self.shell

