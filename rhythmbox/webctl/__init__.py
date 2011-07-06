# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
Basic JSON webserver for Rhythmbox
"""
from __future__ import division, absolute_import, with_statement
import gobject, gtk, gio
import json
from .server import Server

try:
	from rb import Plugin
except ImportError:
	Plugin = object #Testing only

class WebCtl(Plugin):
	def __init__(self):
		super(WebCtl, self).__init__()
	
	def _load_config(self):
		fn = self.find_file("config.json")
		f = gio.File(fn)
		self.config = json.load(f.read())
	
	def activate(self, shell):
		self.shell = shell
		# Load config file
		self._load_config()
		# Start the webserver
		self.server = Server(rbshell=shell, **self.config)
		self.server.__enter__() # Start the server
	
	def deactivate(self, shell):
		self.server.__exit__(None, None, None) # Make sure the server cleans up, need it to remove the reference to shell
		del self.server
		del self.shell

