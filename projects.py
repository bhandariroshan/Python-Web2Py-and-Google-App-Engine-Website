import users

##### project stuff

def blog_key(name = 'default'):
    return users.db.Key.from_path('blogs', name)

class Post(users.db.Model):
	title = users.db.StringProperty(required = True)
	subject = users.db.StringProperty(required = True)
	content = users.db.TextProperty(required = True)
	created = users.db.DateTimeProperty(auto_now_add = True)
	last_modified = users.db.DateTimeProperty(auto_now = True)
	added_by= users.db.StringProperty(required = True)
	project_members = users.db.StringProperty(required=True)
	
	
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return users.render_str("projects.html", p = self, id=self.key().id())
		
	def as_dict(self):
		time_fmt = '%c'
		d = {'title':self.title,
			 'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt),
			 'added_by':self.added_by,
			 'project_members':self.project_members}
		return d
	

class addProjectHandler(users.BlogHandler):
	def get(self):
		if self.user:
			self.user_name=self.request.get('username')
			self.render("addproject.html",user=self.user_name)
			#self.redirect("/adminlogin")
		else:
			#self.render("addproject.html", user = self.request.get('username'))
			self.redirect("/adminlogin")
		
	def post(self):
		if not self.user:
			self.redirect('/adminlogin')
		
		title = self.request.get('title')
		subject = self.request.get('subject')
		content = self.request.get('content')
		project_members=self.request.get('members')
		
		if subject and content and title and project_members:
			p = Post(parent = blog_key(), subject = subject, content = content, title=title,added_by=self.request.get('username'),project_members=project_members)
			p.put()
			self.redirect('/portfolio/%s' % str(p.key().id()))
			#self.redirect('/portfolio')
		else:
			self.render("addproject.html", subject=subject, content=content, title=title,members=project_members, error=error)

class BlogFront(users.BlogHandler):
    def get(self):
		posts = greetings = Post.all().order('-created')
		count = Post.all().count()
		if self.format == 'html':
			self.render('portfolio.html', posts = posts,count = count)
		else:
			return self.render_json([p.as_dict() for p in posts])

class PostPage(users.BlogHandler):
    def get(self, post_id):
        key = users.db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = users.db.get(key)

        if not post:
            self.error(404)
            return
        if self.format == 'html':
            self.render("permalink.html", post = post)
        else:
			self.render_json(post.as_dict())