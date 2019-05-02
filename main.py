from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.Text)
    

    def __init__(self, name, body):
        self.name = name
        self.body = body

@app.route('/', methods = ['POST', 'GET'])
def index():
        blogs = Blog.query.all()
        return render_template ("index.html", title = "Build a Blog", blogs= blogs)

@app.route('/single_blog', methods = ['GET'])
def single_blog():
        blog_id = request.args.get('id') #TODO FIx me?
        blog = Blog.query.filter_by(id = db.blog).first()
        return render_template ("single_blog.html", blog = blog)


@app.route('/newpost', methods=['POST' 'GET'])
def create_new_post():
    name = ""
    body = ""
    name_error = ""
    body_error = "" 

    if request.method == 'GET':
        return render_template("newpost.html", title= "Add Blog Entry")

    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']

        if name == "":
            name_error = "Please enter a title!"

        if body == "":
            body_error = "Please enter a post!"


        if name_error == "" and body_error == "":
            return render_template('newpost.html', title = "Add a new post",
             name_error = name_error, body_error = body_error)
        elif name_error and not body_error:
            return render_template('newpost.html', title = "Add a new post",
            name_error = name_error, body = body )
        elif body_error and not name_error:
            return render_template('newpost.html', title = "Add a new post",
            body_error = body_error, name = name)
        else:
            newpost = Blog(name, body)
            db.session.add(newpost)
            db.session.commit()
            
            return redirect('/single_blog.html?id='+str(newpost.id))




if __name__ == "__main__":
    app.run()
