from operator import le
from os import replace
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import psycopg2
import hashlib, uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager
from flask import request, redirect, url_for, render_template
from sqlalchemy.orm import query
#from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

app = Flask(__name__)
connection = psycopg2.connect(user = "bilalk",
host = "localhost",
port = "5432",
database = "todolist")

cursor = connection.cursor()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bilalk:bilal123@localhost/todolist'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'everything-starts-with-hello-world'

db = SQLAlchemy(app)

class users(db.Model):
    user_name= db.Column(db.String(50), nullable = False,primary_key=True)
    first_name = db.Column(db.String(50),  nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, user_name, first_name, password):
        self.user_name = user_name
        self.first_name = first_name
        self.password = password

@app.route('/')
def index():
    return render_template('index1.html')
    #return '<a href="/signup"><button> Click here </button></a>'

@app.route("/signup", methods=['POST','GET'])
def addperson():
    return render_template("signup1.html")

@app.route("/signup-done", methods=['POST'])
def personadd():
    try:
        print ('\n\n call here \n\n')
        user_name = request.form["user_name"]
        first_name = request.form["first_name"]
        password = request.form["password"]
        print (user_name,first_name,password)
        
        # salt = uuid.uuid4().hex
        # password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # print ('hashedpassword========== ',password)


        entry = users(user_name, first_name,password)
        print (entry)
        db.session.add(entry)
        db.session.commit()

        return render_template("index1.html")
    except Exception as error:
        return repr(error)
        #return 'Lol, Trying SQL Injection?'


@app.route("/login1")
def log_in():
    return render_template("login1.html")


@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["password"]

        print(len(user_name))
        if (len(user_name) == 0 or len(password)==0):
            return "Lol, Are you trying SQL Injection?"

        #print ('USERName----',user_name,password)
        query = """Select * from users where user_name= '%s'  """ %user_name
        print ('q', query)
        out = cursor.execute(query)
        context_record = cursor.fetchall()
        recordKeys = []
        is_login = False
        for row in context_record:
            recordKeys.append(row[2])
        print (recordKeys)
        if len(recordKeys) == 0:
            return 'Wrong Password!'
        if recordKeys[0] == password:
            print ('Password matched!')
            session['user_name'] = user_name
            is_login = True
            #return 'work fine!'
            return redirect(url_for("task"))
            #return render_template('taskhome.html') #Page with two options, View and ADD the taks.

        return render_template('login1.html')    
    return render_template('login1.html')

@app.route('/task')   #Viewtask. add task.
def task():
    return render_template('task_page1.html')

@app.route('/add-task-page')   #Adding the tasks page!
def add_task():
    return render_template('add_tasks_page1.html')

@app.route('/adding_task', methods=['POST','GET'])   #Adding the tasks page!
def adding_task():
    if "user_name" in session and request.method == "POST":
        task_description = request.form["task_description"]
        tag = request.form["tag"]
        due_date = request.form["datee"]

        thistuple = (session["user_name"],tag,due_date,task_description)
        queryy = "Insert into tasks values" + str(thistuple) + ";"
        querryy = """ %s """%queryy 
        cursor.execute(querryy)
        connection.commit()
        return render_template('task_page1.html')
    else:
        return 'Something went wrong in adding task page!'

@app.route('/view-task', methods=['GET'])
def view_tasks():
    if "user_name" in session: 
        query = """ select tag, date,task_description from tasks where user_name= '%s';  """ %session['user_name']                            #query to view the all available tasks with no specific conditions!
        cursor.execute(query)
        records = cursor.fetchall()
        records = tuple(records)
        headings = ("TAG", "DATE", "TASK")
        data = records

        print(records)
        if (len(records)== 0): #if no tasks found
            return "No tasks found!"
        connection.commit()
        return render_template('viewtasks1.html', headings=headings, data=data)
    else:
        return 'Something went wrong in VIEW tasks'

@app.route('/delete-task-page')   #Adding the tasks page!
def delete_task():
    if "user_name" in session:
        return render_template('delete_tasks_page1.html')
    else:
        return 'User not logged in'

@app.route('/deleting_task', methods=['POST', 'GET'])   #Adding the tasks page!
def deleting_task():
    if "user_name" in session:
        delete_description = str(request.form["task_description"])

        query =  """ DELETE FROM tasks WHERE user_name='replace1' and task_description='replace2';   """ 
        query = query.replace('replace1', session['user_name'])
        query = query.replace('replace2',delete_description)

        delete_ = cursor.execute(query)
        connection.commit()
        #print(delete_)
        return 'Task Deleted Successfully!'
        #return delete_

    else:
        return "user not logged in in deleting_task"


@app.route("/helloworld")
def helloworld():
    if "user_name" in session:
        print ("test", session)
        test = session['user_name']

        headings = ("Name", "Bilal", "salary")
        data = (
            ("ROlf","Software","45,000"),
            ("ROlf1","Software1","46,000"),
            ("ROlf2","Software2","48,000"),
        )

        return render_template('helloworld.html', headings=headings, data=data)
    else:
        return render_template('login1.html')

@app.route('/logout')
def logout():
    session.pop("user_name", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run (debug=True)