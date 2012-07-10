import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

def valid_username(s):
	regexp = r"^[a-zA-Z0-9_-]{3,20}$"
	return re.match(regexp,s)

def valid_password(s):
	regexp = r'^.{3,20}$'
	return re.match(regexp,s)

def valid_email(s):
	regexp = r'^[\S]+@[\S]+\.[\S]+$'
	return re.match(regexp,s)

class Signup(BaseHandler):
	def get(self):
		self.render("signup-form.html")

	def post(self):
		have_error = False
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		params = dict(username = username,
						email = email)

		if not username or not valid_username(username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not password or not valid_password(password):
			params['error_password'] = "That's not a valid password."
			have_error = True

		if not verify or password != verify:
			params['error_verify'] = "Your passwords don't match."
			have_error = True

		if email and not valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render("signup-form.html", **params)
		else:
			self.redirect('/welcome?username=' + username)

class Welcome(BaseHandler):
	def get(self):
		username = self.request.get('username')
		if valid_username(username):
			self.render("welcome.html", username = username)
		else:
			self.redirect('/signup')

app = webapp2.WSGIApplication([('/', Signup),
                               ('/welcome', Welcome)],
                              debug=True)