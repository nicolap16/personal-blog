from flask import render_template, url_for, request, redirect, flash
from blog import app, db
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, CommentForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home():
  posts=Post.query.order_by(Post.date.desc()).limit(2).all()
  # Code for limit method from https://www.youtube.com/watch?v=BJeiVGAvEFI
  #   accessed on 17.03.2021 and combined with an order_by method (see below)
  return render_template('home.html',posts=posts)

@app.route("/about")
def about():
  return render_template('about.html', title='About')

@app.route("/all-posts")
def all_posts():
  posts=Post.query.order_by(Post.date.desc()).all()
  return render_template('all_posts.html', title='All Posts: Most Recent', posts=posts)
# # Code for posts appearing in descending order from https://stackoverflow.com/questions/35096259/getting-sorted-results-in-flask-sqlalchemy
#   accessed on 08.03.2021. 

@app.route("/all-posts-asc")
def all_posts_asc():
  posts=Post.query.order_by(Post.date.asc()).all()
  return render_template('all_posts_asc.html', title='All Posts: Oldest', posts=posts)


@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  comments = Comment.query.filter(Comment.post_id==post.id)
  form = CommentForm()
  return render_template('post.html',post=post,comments=comments,form=form)

@app.route('/post/<int:post_id>/comment',methods=['GET','POST'])
@login_required
def post_comment(post_id):
  post=Post.query.get_or_404(post_id)
  form=CommentForm()
  if form.validate_on_submit():
    db.session.add(Comment(content=form.comment.data,post_id=post.id,author_id=current_user.id))
    db.session.commit()
    flash("Your comment has been added to the post","success")
    return redirect(f'/post/{post.id}')
  comments=Comment.query.filter(Comment.post_id==post.id)
  return render_template('post.html',post=post,comments=comments,form=form)

@app.route("/register",methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(first_name=form.first_name.data, surname=form.surname.data, username=form.username.data,email=form.email.data,password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful! Please login in to continue')
    return redirect(url_for('home'))
  return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('Login successful!')
      return redirect(url_for('home'))
    flash('Invalid email address or password.')
    
    return render_template('login.html',form=form)

  return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash('You are now logged out.')
  return redirect(url_for('home'))
