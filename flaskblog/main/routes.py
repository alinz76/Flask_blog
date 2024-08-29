from flask import Blueprint
from flaskblog import db
from flask import render_template, url_for, flash, redirect, request
from flaskblog.posts.forms import PostForm
from flaskblog.posts.models import Post
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # type: ignore
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('home.html', posts=posts, form=form, pagination=posts)


@main.route('/about/')
def about():
    return render_template('about.html')
