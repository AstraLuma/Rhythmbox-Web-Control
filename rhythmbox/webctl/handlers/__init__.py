# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
The root of the handlers
"""
from __future__ import division, absolute_import, with_statement

class example(object):
	"""
	Handler for path /example
	"""
	def GET(self, request, method, url, headers, payload):
		# Send code
		yield 200 # This is the default, so this is optional
	
		# Additional headers to send
		yield 'X-Spam', 'Eggs'
		yield {'X-Foo': 'Bar', 'X-Baz': 'Quux'}
	
		# Send body (JSON, in this case)
		yield {'status': 'ok'}
