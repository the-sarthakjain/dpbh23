from flask import Flask , render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable=False)
    desc = db.Column(db.String(500) , nullable=False)
    date_created = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} + {self.title}"

@app.route('/', methods=["GET" , 'POST'])
def hello_world():
    if request.method == "POST":
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo(title=title , desc = desc)
        
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    
    return render_template("index.html" , allTodo=allTodo) #addd ur html file
    

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is my products page!'

@app.route('/update/<int:sno>', methods=["GET" , 'POST'])
def update(sno):
    if request.method == "POST":
        Time = (request.form['title'])
        desc = (request.form['desc'])
        
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = Time
        todo.desc = desc
        
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html" , todo=todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    
@app.route('/search')
def search():
    q = request.args.get("q")
    print(q)
    if q:
       results = Todo.query.filter(Todo.title.icontains(q) | Todo.desc.icontains(q)).order_by(Todo.date_created.asc()).all()
       
    
    else:
        results = []
    
    return render_template("search.html" , results = results)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



