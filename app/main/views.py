from flask import render_template,redirect,url_for,abort
from . import main
from .. import db
from ..models import Blog,User,Comments
from flask_login import login_required, current_user
from .forms import BlogForm, CommentForm
import markdown2


# index page
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    blogs = Blog.get_blog()
    title = 'Home - Welcome to Blogs Patrol'
    return render_template('index.html', title = title, blogs = blogs)


# Admin dashboard
@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    '''
    Prevent users from accessing the admin page
    '''
    if not current_user.is_admin:
        abort(403)
    else:
        blogs = Blog.get_blog()

    return render_template('admin/admin_dashboard.html', title="AdminDashboard", blogs=blogs)

# single blog
@main.route('/blogs/<int:id>')
def single_blog(id):
    '''
    Function that handles viewing a single review
    '''
    blogs=Blog.query.get(id)


    format_blog = markdown2.markdown(blogs.content,)

    return render_template('blog.html',blogs=blogs)
@main.route('/blog/new/<int:id>', methods = ['GET','POST'])
def new_comment(id):
    '''
    New comment function that returns a form to create a comment on a new page
    '''
    blogs = Blog.query.filter_by(id=id).first()


    form = CommentForm()

    if form.validate_on_submit():
        comment_section = form.comment_section.data
        new_comment = Comments(comment_section=comment_section, blog_id=blogs.id)
        new_comment.save_comment()

        return redirect(url_for('.single_blog', id = blogs.id))

    title = 'New Comment'
    return render_template('new_comment.html', title=title, comment_form=form)

# switch to blogger page
@main.route('/blog')
@login_required
def blogger():
    '''
    Blogger function that returns the  blogger's page and all its data
    '''
    title = 'Blogger'
    blogs = Blog.get_blog()

    return render_template('blogger_post.html', title=title, blogs=blogs)