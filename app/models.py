
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    '''
    Given *user_id*, return the associated User object.
    
    '''
    return User.query.get(int(user_id))

# collection of all blogs
class Blog(db.Model):
    '''
    Blog class define Blog
    '''
    __tablename__ = 'blog'

    # add columns
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment_id = db.relationship("Comments", backref = "blog", lazy = "dynamic")

    # save
    def save_blog(self):
        '''
        Function that saves Blog
        '''

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blog(cls):
        '''
        Function that returns all the data from blog after being queried
        '''
        blog = Blog.query.order_by(Blog.id.desc()).all()
        return blog

    @classmethod
    def delete_blog(cls):
        '''
        Functions the deletes a blog post
        '''
        blog = Blog.query.filter_by(id=blog_id).delete()
        comment = Comments.query.filter_by(blog_id=blog_id).delete()

# users
class User(UserMixin,db.Model):
    '''
    User class that will help to create new users
    '''
    __tablename__ = 'users'

    # add columns
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True,index=True)
    pass_secure = db.Column(db.String(255))
    blog = db.relationship("Blog", backref = "user", lazy = "dynamic")
    comment = db.relationship("Comments", backref = "user", lazy = "dynamic")
    is_admin = db.Column(db.Boolean,default=False)


    # securing our passwords
    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()



    def __repr__(self):
        return f'User {self.username}'

# comments
class Comments(db.Model):
    '''
    comment class that creates new comments from users
    '''
    __tablename__ = 'comment'

    # add columns
    id = db.Column(db. Integer,primary_key = True)
    comment_section = db.Column(db.String(500))
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer,db.ForeignKey("blog.id"))

    def save_comment(self):
        '''
        save the comments per blog
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self,id):
        comment = Comments.query.filter_by(blog_id=id).all()
        return comment

    @classmethod
    def delete_comment(cls,comment_id):
        '''
        Function that delete a simgle comment in a blog post
        '''
        comment = Comments.query.filter_by(id=comment_id).delete()
        db.session.commit()

