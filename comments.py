
import projects

class Comment(projects.users.db.Model):
	postid= projects.users.db.IntegerProperty(required = True)
	commentdate = projects.users.db.DateTimeProperty (auto_now_add = True)
	commenttext = projects.users.db.TextProperty(required = True)
	commentername = projects.users.db.StringProperty(required = True)
	
	
class CommentHandler(projects.users.BlogHandler):
	def get(self):
		postid=int(self.request.get('postid'))
		post=projects.Post.get_by_id(postid,projects.blog_key())
		#comments = Comment.all()
		#comments.filter("postid=" , postid)
		#comments.order('-commentdate')
		comments = projects.users.db.GqlQuery ("SELECT * FROM Comment WHERE postid =" + str(postid) +" ORDER BY commentdate ASC")
		#count = projects.users.db.GqlQuery("Select count(*) FROM Comment WHERE postid =" + str(postid))
		count = Comment.all().filter('postid ==', postid).count()
		self.render("comments.html",post=post,comments=comments,count = count)
	
	def post(self):
		Comment(postid = int(self.request.get('postid')), commenttext = self.request.get('comment'), commentername = self.request.get('name')).put()
		self.redirect('/comments/?postid=' + self.request.get('postid'))
		
	