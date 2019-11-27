import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "notices.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

app.secret_key = "Alisha"

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/", methods=["GET", "POST"])
def hello():
    return render_template('home.html')

@app.route("/create_notice", methods=["GET", "POST"])
def create_notice():
    if request.form:
        notice = Notice(title=request.form.get("title"), body=request.form.get("msg"))
        db.session.add(notice)
        db.session.commit()
        flash("Notice Created Successfully")
    return render_template("create.html")


@app.route("/notice")
def view_notice():
    notices = Notice.query.all()
    # print(notices[id])
    for notice in notices:
        print(notice.id)
    return render_template("notice.html", notices=notices)

@app.route("/edit_notice", methods=["GET","POST"])
def edit_notice():
    if request.form:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        newbody = request.form.get("newbody")
        oldbody = request.form.get("oldbody")
        noticet = Notice.query.filter_by(title=oldtitle).first()
        noticeb = Notice.query.filter_by(body=oldbody).first()
        noticet.title = newtitle
        noticeb.body = newbody
        db.session.commit()
        flash("Notice updated Successfully")
    notices = Notice.query.all()
    return render_template('edit.html', notices=notices)

@app.route("/delete", methods=["POST"])
def delete():
    notice_id = request.form.get("notice_id")
    db.engine.execute('delete from notice where id=:val',{'val':notice_id})
    db.session.commit()
    flash("Notice Deleted Successfully")
    return redirect(url_for('edit_notice'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)