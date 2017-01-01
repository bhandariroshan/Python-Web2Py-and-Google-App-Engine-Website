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

import comments
		
class MainHandler(comments.projects.users.BlogHandler):
    def get(self):
        self.render("aboutme.html")

class contactHandler(comments.projects.users.BlogHandler):
	def get(self):
		self.render("contacts.html")
		
class resumeHandler(comments.projects.users.BlogHandler):
	def get(self):
		self.render("resume.html")


app = comments.projects.users.webapp2.WSGIApplication([('/', MainHandler),
							  ('/contacts',contactHandler),
							  ('/resume',resumeHandler),							  
							  ('/adminlogin',comments.projects.users.adminLoginHandler),
							  ('/signup',comments.projects.users.Register),
							  ('/logout', comments.projects.users.Logout),
							  ('/addproject/?',comments.projects.addProjectHandler),
							  ('/portfolio/?(?:.json)?', comments.projects.BlogFront),
                              ('/portfolio/([0-9]+)(?:.json)?', comments.projects.PostPage),
							  ('/comments/?', comments.CommentHandler)
							  ],
                              debug=True)
