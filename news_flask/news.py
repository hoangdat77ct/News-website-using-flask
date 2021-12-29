from flask import Flask, blueprints, config, render_template, request, redirect, url_for, flash, Blueprint
import math
from werkzeug.exceptions import abort
from news_flask.db import query_select

news = Blueprint("news",__name__)


@news.route('/')
def index():
    try:
        page = int(request.args.get('page', 1))
        page_size = 30
        start = (page - 1) * page_size
        sql = "SELECT * FROM articles LIMIT %s OFFSET %s"
        adr = (page_size,start, )
        posts = query_select(sql,adr)
        sql_count = "SELECT Count(id) FROM articles"
        pages = query_select(sql_count)
        pages = int(pages[0][0])/page_size
    except:
        abort(500)
    return render_template('index.html', posts=posts, pages=math.ceil(pages))
