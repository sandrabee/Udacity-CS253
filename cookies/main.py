#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import hashlib

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
    	self.response.headers['Content-Type'] = 'text/plain'
    	visits = self.request.cookies.get('visits',0)
    	if type(visits) == int or visits.isdigit():
    		visits =  int(visits) + 1
    	else: 
    		visits = 0
        self.response.headers.add_header('Set-Cookie', 'visits = %s'%visits)
        if visits > 10:
            self.write("You have been here often. Thanks!")
        else:
            self.write('You\'ve been here: %s'%visits)
        
        

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
