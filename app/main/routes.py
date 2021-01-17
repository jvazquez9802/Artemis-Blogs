from flask import render_template, request, Blueprint
from app.models import Blog

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.paginate(page=page, per_page=4)
    return render_template('home.html', blogs=blogs)
@main.route("/about")
def about():
    return render_template('about.html')