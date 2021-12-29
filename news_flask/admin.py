from flask import render_template, request, redirect, url_for, flash, Blueprint
import math
from werkzeug.exceptions import abort
from news_flask.db import query_select, query_CUD


bp = Blueprint("admin",__name__)


@bp.route('/admin')
def admin():
    try:
        page = int(request.args.get('page', 1))
        page_size = 30
        start = (page - 1) * page_size
        sql = "SELECT * FROM articles LIMIT %s OFFSET %s"
        adr = (page_size,start, )
        articles = query_select(sql,adr)
        sql_count = "SELECT Count(id) FROM articles"
        pages = query_select(sql_count)
        pages = int(pages[0][0])/page_size
    except:
        abort(500)
    return render_template("admin/admin.html", articles = articles, pages=math.ceil(pages))


@bp.route('/admin/insert', methods = ['POST'])
def insert_news():
    if request.method == 'POST':
        try:
            sql = '''
            INSERT INTO `articles`(`url`, `title`, `authors`, `tags`, `summary`, `publish_date`,
            `image_url`, `domain`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            url = request.form['url']
            title = request.form['title']
            authors = request.form['authors']
            tags = request.form['tags']
            summary = request.form['summary']
            publish_date = request.form['date']
            image_url = request.form['url_image']
            domain = request.form['domain']
            adr = (url,title,authors,tags,summary,publish_date,image_url,domain, )
            query_CUD(sql,adr)
        except:
            abort(403)
        return redirect(url_for('admin.admin'))


@bp.route('/admin/update', methods = ['GET', 'POST'])
def update_news():
    if request.method == 'POST':
        sql = '''
        UPDATE `articles` SET `url`=%s,`title`=%s,
        `authors`=%s,`tags`=%s,`summary`=%s,`publish_date`=%s,`image_url`=%s,`domain`=%s
        WHERE id=%s
        '''
        id = request.form["id"]
        url = request.form['url']
        title = request.form['title']
        authors = request.form['authors']
        tags = request.form['tags']
        summary = request.form['summary']
        publish_date = request.form['date']
        image_url = request.form['url_image']
        domain = request.form['domain']
        adr = (url,title,authors,tags,summary,publish_date,image_url,domain,id, )
        query_CUD(sql,adr)
        return redirect(url_for('admin.admin'))


@bp.route('/admin/delete/<id>/', methods = ['GET', 'POST'])
def delete_news(id):
    sql = "DELETE FROM articles WHERE id=%s"
    adr = (id, )
    query_CUD(sql,adr)
    return redirect(url_for('admin.admin'))