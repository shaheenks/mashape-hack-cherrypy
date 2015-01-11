#!/usr/bin/python

import os, os.path
import random
import string
import time

import cherrypy

import unirest

def wget(func):
	base='https://currency-exchange.p.mashape.com/'
	key={"X-Mashape-Key": "20kSqyduznmsh0uKE8zpTY1ri8U3p1Ks8DcjsnMwtJAvqfpN2e"}
	try:
	  response = unirest.get(base+func, headers=key)
	  if response.code == 200:
		  return response.body
	except IOError:
		print time.strftime('%Y-%m-%d %H:%M:%S %Z'), ': Problem reading url:', url
		
def convert(src, dest, amt):
	rate = wget('exchange?'+'from='+src+'&to='+dest+'&q='+amt)
	return rate, dest, src, float(amt)*rate
	
def quotes():
	return ' '.join(wget('listquotes'))

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return '<html><head></head><body><p>Currency Converter</p><p>%s</p><form method="get" action="generate">From:<input type="text" value="EUR" name="src" /><br><br>To:<input type="text" value="USD" name="dest" /><br><br>Amount:<input type="Number" value="1" name="amt" /><br><br><button type="submit">Give it now!</button></form></body></html>' % (quotes())

    @cherrypy.expose
    def generate(self, src=8, dest=8, amt=8):
        some_string = convert(src, dest, amt)
        cherrypy.session['mystring'] = some_string
        return 'Rate : %f %s / %s,  > Total Amount : %f' % (some_string)
        
    @cherrypy.expose
    def display(self):
		return cherrypy.session['mystring']

if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		}
	}
	cherrypy.quickstart(StringGenerator(), '/', conf)
