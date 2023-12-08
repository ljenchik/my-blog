from flask import render_template

from app import app

@app.route('/')
@app.route('/home')
# @login_required
def index():
    # posts = Post.query.all()
    return render_template("index.html", title='Home Page')
