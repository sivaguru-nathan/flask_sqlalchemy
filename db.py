from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

db = SQLAlchemy()

class User(db.Model):
    __tablename ='users' 
    id=db.Column('id', db.Integer,primary_key=True,nullable=False)
    firstName=db.Column('firstName' ,db.Text)
    nickName=db.Column('nickName' ,db.Text)
    lastName=db.Column('lastName' ,db.Text)
    email=db.Column('email' ,db.Text,nullable=False)
    password=db.Column('password' ,db.Text,nullable=False)
    avatar=db.Column('avatar' ,db.VARCHAR(255) ,default='')
    signupTimestamp=db.Column('signupTimestamp', db.DATETIME,nullable=True ,default=dt.now())
    newFeatureEmail=db.Column('newFeatureEmail', db.SMALLINT ,default='0')
    changeAllocationEmail=db.Column('changeAllocationEmail', db.SMALLINT ,default='0')
    loginActivityEmail=db.Column('loginActivityEmail', db.SMALLINT ,default='0')
    appIntro=db.Column('appIntro', db.SMALLINT,nullable=False ,default='0')
    lbShareAllocDate=db.Column('lbShareAllocDate', db.DATETIME,nullable=True ,default='9999-12-31 23:59:59')
    lbParticipationDate=db.Column('lbParticipationDate', db.DATETIME,nullable=True ,default='9999-12-31 23:59:59')
    