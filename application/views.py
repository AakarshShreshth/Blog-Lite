from flask import request, render_template, flash, url_for, redirect, Response
from flask import current_app as app
from flask_login import login_required, current_user
from application.database import db
from application.models import User, Post, Follow
from werkzeug.utils import secure_filename

# Views
# --begin
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    follow = Follow.query.filter_by(user_id=current_user.id).with_entities(Follow.follows_id).all()
    following = [f[0] for f in follow]
    all_posts = Post.query.order_by(db.desc(Post.date_created)).all()
    posts = []
    for post in all_posts:
        if post.author in following:
            posts.append(post)
    return render_template("home.html", posts=posts, get_img=get_img)

@app.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.files['image']
        if not title:
            flash('Title cannot be empty!', category='error')
        elif not description:
            flash('Description cannot be empty!', category='error')
        elif not image:
            flash('No image uploaded!', category='error')
        else:
            filename = secure_filename(image.filename)
            mimetype = image.mimetype
            if not filename:
                flash('Image has no filename', category='error')
            else:
                post = Post(title=title, description=description, image=image.read(), filename=filename, mimetype=mimetype, author=current_user.id)
                db.session.add(post)
                db.session.commit()
                print()
                print(title, description, filename, mimetype, sep='\n')
                print()
                flash('Post created', category='success')
                return redirect(f"/user/{current_user.username}")
    return render_template("create_post.html")

@app.route('/img/<int:id>')
def get_img(id):
    img = Post.query.filter_by(id=id).first()
    return Response(img.image, content_type=img.mimetype)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    following = Follow.query.filter_by(user_id=user.id).all()
    followers = Follow.query.filter_by(follows_id=user.id).all()

    if (not user) and current_user != user:
        flash('User does not exist!', category='error')
        return redirect(url_for('.home'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("user_profile.html", user=user, posts=posts, get_img=get_img, username=username, followers=followers, following=following)

@app.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash("You don't have permission to delete this post!", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', category="success")
    return redirect(f'/user/{current_user.username}')

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    following = Follow.query.filter_by(user_id=current_user.id).filter_by(follows_id=user.id).first()

    if following:
        flash(f'You already follow {username}', category='error')
    else:
        follow = Follow(user_id=current_user.id, user_name=current_user.username, follows_id=user.id, follows_name=user.username)
        db.session.add(follow)
        db.session.commit()
        flash(f'You started following {username}', category='success')
    return redirect(f"/user/{username}")

@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    follow = Follow.query.filter_by(user_id=current_user.id).filter_by(follows_id=user.id).first()
    db.session.delete(follow)
    db.session.commit()
    flash(f'You unfollowed {username}', category='success')
    return redirect(f'/user/{current_user.username}')

@app.route("/user/<int:id>/following/")
@login_required
def following(id):
    user = User.query.filter_by(id=id).first()
    following = Follow.query.filter_by(user_id=user.id).all()
    follow = Follow.query.filter_by(user_id=current_user.id).with_entities(Follow.follows_id).all()
    follow_list = [f[0] for f in follow]
    return render_template("following.html", user=user, following=following, follow_list=follow_list)

@app.route("/user/<int:id>/followers")
@login_required
def followers(id):
    user = User.query.filter_by(id=id).first()
    followers = Follow.query.filter_by(follows_id=user.id).all()
    follow = Follow.query.filter_by(user_id=current_user.id).with_entities(Follow.follows_id).all()
    follow_list = [f[0] for f in follow]
    return render_template("followers.html", user=user, followers=followers, current_user=current_user, follow_list=follow_list)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    results = None
    follow = Follow.query.filter_by(user_id=current_user.id).with_entities(Follow.follows_id).all()
    follow_list = [f[0] for f in follow]
    if request.method == "POST":
        q = request.form.get("query")
        if q == "":
            flash("Enter a username", category='error')
        else:
            query = "%"+q+"%"
            results = User.query.filter(User.username.like(query)).all()
            if  not results:
                flash("No user found", category="error")
    
    return render_template("search.html", results=results, follow_list=follow_list)
# --end