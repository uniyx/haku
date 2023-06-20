# haku/routes.py

from datetime import datetime
from flask import abort, jsonify, render_template, url_for, flash, redirect, request
from psycopg2 import IntegrityError
from haku import app, db, bcrypt
from haku.forms import RegistrationForm, LoginForm, PostForm, CommunityForm
from haku.models.user import User
from haku.models.post import Post
from haku.models.community import Community
from haku.models.vote import Vote
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

@app.route("/")
def home():
    print(current_user)
    posts = Post.query.order_by(Post.date_posted.desc()).all()  # Query all posts in descending order by date
    return render_template('home.html', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(current_user)
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/c/<community_name>/<int:post_id>")
@login_required
def post(community_name, post_id):
    community = Community.query.filter_by(name=community_name).first_or_404()
    post = Post.query.get_or_404(post_id)
    if post.community_id != community.id:
        abort(404)
    return render_template('post.html', title=post.title, post=post, community=community)

@app.route("/submit", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, community=form.community.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('submit.html', title='New Post', form=form, legend='New Post')

@app.route("/user/<string:username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .all()
    return render_template('profile.html', posts=posts, user=user)

@app.route("/create_community", methods=['GET', 'POST'])
@login_required
def create_community():
    form = CommunityForm()
    if form.validate_on_submit():
        community = Community(name=form.name.data, description=form.description.data)
        db.session.add(community)
        db.session.commit()
        flash('Your community has been created!', 'success')
        return redirect(url_for('community', community_name=community.name))
    return render_template('create_community.html', title='Create Community', form=form)

@app.route("/c/<community_name>")
def community(community_name):
    community = Community.query.filter_by(name=community_name).first_or_404()
    posts = Post.query.filter_by(community_id=community.id).order_by(Post.date_posted.desc()).all()
    return render_template('community.html', community=community, posts=posts)

@app.route("/c/<string:community_name>/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(community_name, post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_edited = datetime.utcnow()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', community_name=community_name, post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('submit.html', title='Update Post', form=form, legend='Update Post')

@app.context_processor
def utility_processor():
    def get_post_vote_total(post_id):
        total = db.session.query(func.sum(Vote.value)).filter(Vote.post_id == post_id).scalar()
        return total if total else 0
    return dict(get_post_vote_total=get_post_vote_total)

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    data = request.get_json()
    post_id = data['post_id']
    value = data['value']

    print(post_id, value)

    # Check if the user has already voted
    vote = Vote.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if vote:
        # If the existing vote's value is the same as the new value, remove the vote
        print(vote.value, value)
        if vote.value == int(value):
            vote.value = 0
        else:
            # If the existing vote's value is different from the new value, update the vote
            vote.value = value
    else:
        # If the user has not voted yet, add a new vote
        vote = Vote(user_id=current_user.id, post_id=post_id, value=value)
        db.session.add(vote)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'You have already voted.'}), 400

    new_score = db.session.query(func.sum(Vote.value)).filter(Vote.post_id == post_id).scalar() or 0
    return jsonify({'new_score': new_score, 'value': value}), 200
