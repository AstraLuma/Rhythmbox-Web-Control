# -*- tab-width: 4; use-tabs: 1; coding: utf-8 -*-
# vim:tabstop=4:noexpandtab:
"""
Handlers for controlling the player.
"""
from __future__ import division, absolute_import, with_statement
import rhythmdb

class previous(object):
	def POST(self, request, env, url, headers, payload):
		shell = env['rbshell']
		shell.props.shell_player.do_previous()
		yield {'status': 'ok'}

class next(object):
	def POST(self, request, env, url, headers, payload):
		shell = env['rbshell']
		shell.props.shell_player.do_next() 
		yield {'status': 'ok'}

class pause(object):
	def POST(self, request, env, url, headers, payload):
		shell = env['rbshell']
		shell.props.shell_player.pause()
		yield {'status': 'ok'}

class play(object):
	def POST(self, request, env, url, headers, payload):
		shell = env['rbshell']
		shell.props.shell_player.play()
		yield {'status': 'ok'}

class stop(object):
	def POST(self, request, env, url, headers, payload):
		shell = env['rbshell']
		shell.props.shell_player.stop()
		yield {'status': 'ok'}

class playpause(object):
	def POST(self, request, env, url, headers, payload):
		shell = env['rbshell']
		shell.props.shell_player.playpause()
		yield {'status': 'ok'}

class playing(object):
	def GET(self, request, env, url, headers, payload):
		shell = env['rbshell']
		rv = shell.props.shell_player.get_playing()
		
		props = [
			'PROP_ALBUM', 'PROP_ALBUM_ARTIST', 'PROP_ALBUM_GAIN', 
			'PROP_ALBUM_PEAK', 'PROP_ARTIST', 'PROP_BITRATE', 'PROP_BPM', 
			'PROP_COMMENT', 'PROP_COPYRIGHT', 'PROP_DATE', 'PROP_DESCRIPTION', 
			'PROP_DISC_NUMBER', 'PROP_DURATION', 'PROP_FILE_SIZE', 
			'PROP_FIRST_SEEN', 'PROP_FIRST_SEEN_STR', 'PROP_GENRE', 
			'PROP_HIDDEN', 'PROP_IMAGE', 'PROP_KEYWORD', 'PROP_LANG', 
			'PROP_LAST_PLAYED', 'PROP_LAST_PLAYED_STR', 'PROP_LAST_SEEN', 
			'PROP_LAST_SEEN_STR', 'PROP_LOCATION', 'PROP_MIMETYPE', 
			'PROP_MTIME', 'PROP_PLAYBACK_ERROR', 'PROP_PLAY_COUNT', 
			'PROP_POST_TIME', 'PROP_RATING', 'PROP_SEARCH_MATCH', 
			'PROP_STATUS', 'PROP_SUBTITLE', 'PROP_SUMMARY', 'PROP_TITLE', 
			'PROP_TRACK_GAIN', 'PROP_TRACK_NUMBER', 'PROP_TRACK_PEAK', 
			'PROP_YEAR',
			]
		entry = shell.props.shell_player.get_playing_entry()
		yield {'status': 'ok', 'playing': rv}.update((p, shell.props.db.entry_get(entry, getattr(rhythmdb, p))) for p in props)
