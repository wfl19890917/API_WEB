from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql
from flask_bootstrap import Bootstrap
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:wfl19890917@127.0.0.1:3306/mydatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
# 创建数据库模型类
class User(db.Model):
    __tablename__ = "tbl_users"  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键 
    name = db.Column(db.String(64), unique=True,nullable=False) # 数据库中的字段
    email = db.Column(db.String(64), unique=True,nullable=False)
    password = db.Column(db.String(128),nullable=False)
class Interface(db.Model):
    __tablename__ = 'tbl_interface'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pro_name = db.Column(db.String(225), nullable=True)
    inter_name=db.Column(db.String(225), nullable=True)
    url = db.Column(db.String(225), nullable=True)
    method = db.Column(db.String(225), nullable=True)
    header = db.Column(db.String(225), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
class Case(db.Model):
    __tablename__ = 'tbl_testcase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inter_name = db.Column(db.String(225), nullable=True)
    case_name=db.Column(db.String(225), nullable=True)
    method = db.Column(db.String(225), nullable=True)
    url = db.Column(db.String(225), nullable=True)
    data=db.Column(db.String(225), nullable=True)
    header=db.Column(db.String(225), nullable=True)
    msg=db.Column(db.String(225), nullable=True)
    code=db.Column(db.String(225), nullable=True)
    expect=db.Column(db.String(225), nullable=True)
    status=db.Column(db.String(225), nullable=True)
    actual=db.Column(db.String(225), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())