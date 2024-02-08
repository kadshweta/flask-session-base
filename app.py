from flask import Flask,request,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api




app=Flask(__name__)

app.config['SECRET_KEY']='SUPER-SECRET-KEY'
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///data.db'

db=SQLAlchemy(app)
api=Api(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    password=db.Column(db.String(200))

# db.create_all() 


class User_register(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']

        if not username or not password:
            return {'msg':'missing username or password '},400
        
        if User.query.filter_by(username=username).first():
            return {'msg':'user already taken'},400
        
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'msg':'user created succesfully '},200

class user_login(Resource):
     def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        
        user=User.query.filter_by(username=username).first()
            
        if user and user.password == password:
            session["user_id"]=user.id
            print(session)
            
        return {'msg':'okay'},200
    
api.add_resource(User_register,'/register')
api.add_resource(user_login,'/login')


# @app.route("/update/<int:id>",methods=['POST'])
# def user_update(id):
#     user=database.query.get(id)
#     name = request.json['name']
#     course = request.json['course']
#     comp_name = request.json['comp_name']
#     age = request.json['age']


#     user.name = name
#     user.course = course
#     user.comp_name = comp_name
#     user.age = age

#     db.session.commit()
#     return "done update "







if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)