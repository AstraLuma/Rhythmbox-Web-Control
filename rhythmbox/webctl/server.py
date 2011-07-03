# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
A webserver for serving JSON RPC calls, based on gobject.
"""
from __future__ import division, absolute_import, with_statement
import gobject, glib
import BaseHTTPServer, json, urlparse
import rb # Needed for some metadata
__all__ = 'Server',

JSON_MIMETYPE = 'application/json'

_hasbody = lambda c: c >= 200 and c not in (204, 304)

# Note: The server libraries use old-style classes, the "object" subclassing is to fix that.

class Server(BaseHTTPServer.HTTPServer, object):
# Server management activities
	def __init__(self, **env):
		super(Server, self).__init__(self.env['listen'], RequestHandler, bind_and_activate=False)
		self.env = dict(env)
	
	def __enter__(self):
		# Create socket, start listening
		self.server_bind()
		self.server_activate()
		# Hook into glib (GTK) event loop
		self.glib_source = glib.io_add_watch(self.socket, glib.IO_IN, self._data_in)
	
	def __exit__(self, exc_type, exc_value, traceback):
		# Remove from event loop
		glib.source_remove(self.glib_source)
		del self.glib_source
		# Clean up socket
		self.server_close()
		# Remove references to environment objects (namely, Rhythmbox shell)
		del self.env
	
	def _data_in(self, source, condition)
		self._handle_request_noblock() # We can skip their select() call, since we already know there's data to read
		return True # Continue reading data

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler, object):
	# Configure the request handler
	server_version = 'Rhythmbox/%s WebCtl/0.1' % (rb.__version__)
	protocol_version = 'HTTP/1.1'
	
	def send_error(self, code, message=None, explain=None):
		"""Send and log an error reply.
		
		Arguments are the error code, and a detailed message.
		The detailed message defaults to the short entry matching the
		response code.
		
		This sends an error response (so it must be called before any
		output has been generated), logs the error, and finally sends
		some JSON informing the client of the error
		"""
		# Mostly ripped straight out of the base class
		
		try:
			short, long = self.responses[code]
		except KeyError:
			short, long = '???', '???'
		if message is None:
			message = short
		if explain is None:
			explain = long
		self.log_error("code %d, message %s", code, message)
		# using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
		content = json.dumps({'code': code, 'message': message, 'explain': explain})
		self.send_response(code, message)
		self.send_header("Content-Type", JSON_MIMETYPE)
		self.send_header('Connection', 'close')
		if _hasbody(code):
			self.send_header('Content-Length', len(content)) # Still send with HEAD
		self.end_headers()
		if self.command != 'HEAD' and _hasbody(code):
			self.wfile.write(content)
	
	POST_PARSERS = {
		'application/x-www-form-urlencoded': urlparse.parse_qs,
		# TODO: Add the multipart used in file uploads
		JSON_MIMETYPE: json.loads,
		}
	
	def _parse_payload(self):
		l = self.headers.get('Content-Length', '')
		data = self.rfile.read(l)
		t = self.headers.gettype()
		if t in self.POST_PARSERS:
			return self.POST_PARSERS[t](data)
		else:
			#XXX: Do we want to return an error or something?
			return data
	
	def _find_handler(self):
		path = urlparse.urlparse(self.path, 'http').path
		if path.startswith('/'):
			path = path[1:]
		path = path.split('/')
		
		#FIXME: Do this by repeated getattr() calls
		modname = '.'.join(['handlers']+path[:-1])
		objname = path[-1]
		try:
			module = __import__(modname, globals(), [objname], 1)
			obj = getattr(module, objname)
		except (ImportError, AttributeError):
			# Return a 404, couldn't find the handler
			pass
		#END FIXME
		
		if isinstance(obj, type):
			obj = obj()
		
		cmd = self.command
		if cmd == 'HEAD': # This must process the same as a GET
			cmd = 'GET' # So tell the handler it's a GET
		
		try:
			return getattr(obj, cmd)
		except AttributeError:
			# Return a 405, handler doesn't do this method
			pass
	
	def _dispatch(self):
		headers = self._parse_headers()
		if self.command == 'POST':
			payload = self._parse_payload()
		else:
			payload = None
		
		# Make the call
		h = self._find_handler()(self, urlparse.urlparse(self.path, 'http'), self.headers, payload)
		
		# Make the response
		try:
			data = list(h)
		except Exception, err:
			import traceback
			self.send_error(500, explain=traceback.format_exc())
			return
		else:
			code = 200
			content = ""
			heads = []
			
			# Did they send a code?
			if isinstance(data[0], int) or hasattr(data[0], '__index__'):
				code = data[0]
				del data[0]
			
			# Is there content?
			if _hasbody(code):
				content = data[-1]
				del data[-1]
			
			for d in data:
				if isinstance(d, dict):
					for i in d.items(): heads.append(i)
				else:
					heads.append(d)
			
			hastype = any(n.lower() = 'content-type' for n,_ in heads)
			
			if isintance(content, basestring):
				if not hastype: heads += [('Content-Type', 'text/plain')]
			else: #JSON!
				content = json.dumps(content)
				if hastype: raise RuntimeError, "If a handler gives a type, it needs to return a string"
				heads += [('Content-Type', JSON_MIMETYPE)]
			
			self.send_response(code)
			
			sentlen = False
			for name, val in heads:
				self.send_header(name, val)
				if name.lower() == 'content-length':
					sentlen = True
			if not sentlen and _hasbody(code):
				self.send_header('Content-Length', len(content)) # Still send with HEAD
			self.end_headers()
			
			if self.command != 'HEAD' and _hasbody(code):
				self.wfile.write(content)
	
	do_HEAD = do_GET = do_POST = _dispatch

