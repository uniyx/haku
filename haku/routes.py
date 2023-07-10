# haku/routes.py

from datetime import datetime
from flask import abort, jsonify, render_template, url_for, flash, redirect, request
from psycopg2 import IntegrityError
from haku import app, db, bcrypt
from haku.forms import RegistrationForm, LoginForm, TextPostForm, LinkPostForm, ImagePostForm, UpdateAccountForm, UpdatePasswordForm, CommunityForm
from haku.models.user import User
from haku.models.post import Post
from haku.models.community import Community
from haku.models.vote import Vote
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/", defaults={'sort': 'new'})
@app.route("/<string:sort>")
def home(sort):
    page = request.args.get('page', 1, type=int)
    
    if sort == "new":
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    elif sort == "top":
        posts = Post.query.order_by(Post.votes.desc()).paginate(page=page, per_page=10)
    elif sort == "hot":
        # Implement!
        # posts = hot_sort(Post.query.all())
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    else:
        # Invalid sort type
        abort(404)

    return render_template("home.html", posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Use set_password method to hash the password
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, compact=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form, compact=True)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    account_form = UpdateAccountForm()
    password_form = UpdatePasswordForm()

    if account_form.validate_on_submit():
        print("test 1")
        current_user.email = account_form.email.data
        current_user.bio = account_form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('settings'))

    if password_form.validate_on_submit():
        print("test 2")
        print(password_form.current_password.data)
        if current_user.check_password(password_form.current_password.data):
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('settings'))
        else:
            flash('Current password is incorrect.', 'danger')

    elif request.method == 'GET':
        account_form.email.data = current_user.email
        account_form.bio.data = current_user.bio

    return render_template('settings.html', title='Settings', 
                           user=current_user, account_form=account_form, password_form=password_form)
    
@app.template_filter('nl2br')
def nl2br_filter(s):
    return s.replace('\n', '<br>')

@app.route("/c/<community_name>/<int:post_id>")
@login_required
def post(community_name, post_id):
    community = Community.query.filter_by(name=community_name).first_or_404()
    post = Post.query.get_or_404(post_id)
    if post.community_id != community.id:
        abort(404)
    return render_template('post.html', title=post.title, post=post, community=community, compact=True)

@app.route("/submit", methods=['GET', 'POST'])
@login_required
def submit():
    text_form = TextPostForm(prefix='text')
    link_form = LinkPostForm(prefix='link')
    image_form = ImagePostForm(prefix='image')

    if 'text-submit' in request.form and text_form.validate_on_submit():
        post = Post(post_type='text', title=text_form.title.data, content=text_form.content.data, author=current_user, community=text_form.community.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    elif 'link-submit' in request.form and link_form.validate_on_submit():
        post = Post(post_type='link', title=link_form.title.data, content=link_form.link_url.data, author=current_user, community=link_form.community.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    # elif 'image-submit' in request.form and image_form.validate_on_submit():
    #     if image_form.image_file.data:
    #         picture_file = save_picture(image_form.image_file.data)
    #         post = Post(post_type='image', title=image_form.title.data, content=picture_file, author=current_user, community=image_form.community.data)
    #         db.session.add(post)
    #         db.session.commit()
    #     return redirect(url_for('home'))

    return render_template('submit.html', title='Submit Post', text_form=text_form, link_form=link_form, image_form=image_form, compact=True)

@app.route("/u/<string:username>/", defaults={'sort': 'new'})
@app.route("/u/<string:username>/<string:sort>")
def profile(username, sort):
    user = User.query.filter_by(username=username).first_or_404()
    posts_query = Post.query.filter_by(author=user)
    page = request.args.get('page', 1, type=int)

    if sort == "new":
        posts = posts_query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    elif sort == "top":
        posts = posts_query.order_by(Post.votes.desc()).paginate(page=page, per_page=10)
    elif sort == "hot":
        #Implement
        #posts = hot_sort(posts_query.all())
        posts = posts_query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    else:
        abort(404)
    return render_template("profile.html", posts=posts, user=user, compact=True)

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

@app.route("/c/<string:community_name>/", defaults={'sort': 'new'})
@app.route("/c/<string:community_name>/<string:sort>")
def community(community_name, sort):
    community = Community.query.filter_by(name=community_name).first_or_404()
    posts = Post.query.filter_by(community_id=community.id)
    page = request.args.get('page', 1, type=int)

    if sort == "new":
        posts = posts.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    elif sort == "top":
        posts = posts.order_by(Post.votes.desc()).paginate(page=page, per_page=10)
    elif sort == "hot":
        # Implement
        # posts = hot_sort(community.posts.all())
        posts = posts.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    else:
        abort(404)
    return render_template("community.html", community=community, posts=posts)

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
    return render_template('submit.html', title='Update Post', form=form, legend='Update Post', compact=True)

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
    new_value = int(data['value'])
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # check if vote by this user already exists
    vote = Vote.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if vote:
        # If the existing vote's value is the same as the new value, remove the vote
        if vote.value == new_value:
            vote.value = 0
            user_vote = 0
            post.votes -= new_value  # Decrease post votes by the vote value
            post.author.karma -= new_value  # Decrease author's karma by the vote value
        else:
            # if existing vote is not same as new vote, update the vote
            post.votes -= vote.value  # First, remove the value of the old vote from the post votes
            post.author.karma -= vote.value  # First, remove the value of the old vote from the author's karma
            vote.value = new_value
            user_vote = new_value
            post.votes += new_value  # Then, add the value of the new vote to the post votes
            post.author.karma += new_value  # Then, add the value of the new vote to the author's karma
    else:
        # if no existing vote, create a new vote
        vote = Vote(user_id=current_user.id, post_id=post_id, value=new_value)
        db.session.add(vote)
        user_vote = new_value
        post.votes += new_value  # Increase post votes by the vote value
        post.author.karma += new_value  # Increase author's karma by the vote value

    db.session.commit()

    new_score = post.votes
    return jsonify({'new_score': new_score, 'user_vote': user_vote}), 200

@app.context_processor
def utility_processor():
    def get_user_vote(post_id):
        if current_user.is_authenticated:
            vote = Vote.query.filter_by(post_id=post_id, user_id=current_user.id).first()
            return vote.value if vote else 0
        else:
            return None

    return {'get_user_vote': get_user_vote}

@app.route('/save_post', methods=['POST'])
@login_required
def save_post():
    data = request.get_json()
    post_id = data['post_id']
    post = Post.query.get(post_id)
    
    if post in current_user.saved:
        current_user.saved.remove(post)
        saved = False
    else:
        current_user.saved.append(post)
        saved = True

    db.session.commit()
    return jsonify({'saved': saved})

@app.route('/saved')
@login_required
def saved():
    posts = current_user.saved
    return render_template('saved.html', posts=posts, compact=True)
