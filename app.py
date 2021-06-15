# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import login_manager
# from flask import request, redirect, url_for, render_template
# #from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bilalk:bilal123@localhost/todolist'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = 'everything-starts-with-hello-world'

# db = SQLAlchemy(app)


# class users(db.Model):
#     user_name= db.Column(db.String(50), nullable = False,primary_key=True)
#     first_name = db.Column(db.String(50),  nullable=False)
#     password = db.Column(db.String(50), nullable=False)

#     def __init__(self, user_name, first_name, password):
#         self.user_name = user_name
#         self.first_name = first_name
#         self.password = password

# @app.route('/')
# def index():
#     return '<a href="/addperson"><button> Click here </button></a>'

# @app.route("/addperson")
# def addperson():
#     return render_template("index.html")

# @app.route("/personadd", methods=['POST'])
# def personadd():
#     user_name = request.form["user_name"]
#     first_name = request.form["first_name"]
#     password = request.form["password"]
#     print (user_name,first_name,password)
    
#     entry = users(user_name, first_name,password)
#     print (entry)
#     db.session.add(entry)
#     db.session.commit()

#     return render_template("index.html")


# if __name__ == "__main__":
#     db.create_all()
#     app.run (debug=True)