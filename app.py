from flask import Flask,request,jsonify,make_response
from db import *
import json
from alchemyencode import *
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:1234@0.0.0.0:3306/first_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']="foofoo"

@app.before_first_request
def create_tables():
    db.create_all()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user,*args, **kwargs)

    return decorated

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401)

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'email' : user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401)

@app.route('/',methods=['GET'])
def allUser():
    return json.dumps(User.query.all(),cls=AlchemyEncoder)

@app.route('/update',methods=['GET'])
@token_required
def updateUser(current_user):
    key=request.args.get('key')
    value=request.args.get('value')
    user=current_user
    print(id,key,value)
    setattr(user,key,value)
    db.session.commit()
    return json.dumps(User.query.filter_by(id=id).first(),cls=AlchemyEncoder)

@app.route('/create',methods=['POST'])
def createUser():
    data=request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user=User(id=data['id'],firstName=data['firstName'],email=data['email'],password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return json.dumps(User.query.all(),cls=AlchemyEncoder)

@app.route('/delete',methods=['GET'])
@token_required
def deleteUser(current_user):
    user=current_user
    db.session.delete(user)
    db.session.commit()
    return json.dumps(User.query.all(),cls=AlchemyEncoder)

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)