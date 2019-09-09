# -*- coding:utf-8 -*-
from flask import Flask,make_response
from flask import render_template,request,url_for,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql
from flask_bootstrap import Bootstrap
import pymysql
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length
from wsgiref.validate import validator
from dominate.tags import header
from flask import get_flashed_messages,flash
import os
import xlrd
import tablib
from werkzeug.utils import secure_filename
import requests
import unittest
import http_request
from sqlalchemy.sql.expression import false
import xlwt
from io import StringIO,BytesIO
from sqlalchemy.sql.operators import from_
pymysql.install_as_MySQLdb()
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
    status=db.Column(db.String, nullable=True)
    actual=db.Column(db.String(225), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
class Report(db.Model):
    __tablename__ = 'tbl_testreport'
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
    status=db.Column(db.String, nullable=True)
    actual=db.Column(db.String(225), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/interface')
def interface():
    resultlist=Interface.query.all()
    return render_template('interface.html',resultlist=resultlist)
@app.route('/add_interface')
def add_interface():
    return render_template('addinterface.html')
@app.route('/add_interface_success',methods=['GET','POST'])
def add_interface_success():
    if request.method=='GET':
        return render_template('addinterface.html')
    else:
        pro_name=request.form.get('project')
        inter_name=request.form.get('intername')
        url=request.form.get('url')
        meth=request.form.get('meth')
        header=request.form.get('header')
        newinterface=Interface(pro_name=pro_name,inter_name=inter_name,url=url,method=meth,header=header)
        db.session.add(newinterface)
        db.session.commit()
        return redirect(url_for('interface'))
@app.route('/edit_interface/<int:id>',methods=['GET','POST'])
def edit_interface(id):
    inters=Interface.query.filter_by(id=id).all()
    return render_template('editinterface.html',inters=inters)
@app.route('/edit_inter_success/<int:id>',methods=['GET','POST'])
def edit_inter_success(id):
    inter=Interface.query.filter_by(id=id).first()
    if request.method=='POST':
        inter.pro_name=request.form.get('project')
        inter.inter_name=request.form.get('intername')
        inter.url=request.form.get('url')
        inter.method=request.form.get('meth')
        inter.header=request.form.get('header')
        db.session.add(inter)
        db.session.commit()
        return redirect(url_for('interface'))
@app.route('/delete_interface/<int:id>')
def delete_interface(id):
    inter=Interface.query.filter_by(id=id).first()
    db.session.delete(inter)
    db.session.commit()
    return redirect(url_for('interface'))  
@app.route('/yongli')
def yongli():
    resultlist=Case.query.all()
    return render_template('yongli.html',resultlist=resultlist)
@app.route('/add_case')
def add_case():
    return render_template('addcase.html')
@app.route('/add_case_success',methods=['GET','POST'])
def add_case_success():
    if request.method=='GET':
        return render_template('addcase.html')
    else:
        case_name=request.form.get('casename')
        inter_name=request.form.get('intername')
        url=request.form.get('url')
        meth=request.form.get('meth')
        header=request.form.get('header')
        data=request.form.get('data')
        msg=request.form.get('msg')
        code=request.form.get('code')
        expect=request.form.get("expect")
        status=request.form.get('status')
        actual=request.form.get('actual')
        newcase=Case(case_name=case_name,inter_name=inter_name,\
                     url=url,method=meth,data=data,header=header,\
                     msg=msg,code=code,expect=expect,status=status,actual=actual)
        db.session.add(newcase)
        db.session.commit()
        return redirect(url_for('yongli'))
@app.route('/edit_case/<int:id>',methods=['GET','POST'])
def edit_case(id):
    cases=Case.query.filter_by(id=id).all()
    return render_template('editcase.html',cases=cases)
@app.route('/edit_case_success/<int:id>',methods=['GET','POST'])
def edit_case_success(id):
    case=Case.query.filter_by(id=id).first()
    if request.method=='POST':
        case.case_name=request.form.get('casename')
        case.inter_name=request.form.get('intername')
        case.url=request.form.get('url')
        case.meth=request.form.get('meth')
        case.header=request.form.get('header')
        case.data=request.form.get('data')
        case.msg=request.form.get('msg')
        case.code=request.form.get('code')
        case.expect=request.form.get("expect")
        case.status=request.form.get('status')
        case.actual=request.form.get('actual')
        db.session.add(case)
        db.session.commit()
        return redirect(url_for('yongli'))
@app.route('/delete_case/<int:id>')
def delete_case(id):
    case=Case.query.filter_by(id=id).first()
    db.session.delete(case)
    db.session.commit()
    return redirect(url_for('yongli'))  
@app.route('/daoru_ca')
def daoru_ca():
    return render_template('uploadcase.html')
@app.route('/daoru_case',methods=['GET','POST'])
def daoru_case():
    if request.method=='POST':
        file=request.files.get('file')
        f=file.read()
        book=xlrd.open_workbook(file_contents=f)
        sheetnames=book.sheet_names()
        for sheetname in sheetnames:
            sheet=book.sheet_by_name(sheetname)
            nrows=sheet.nrows
            ncols=sheet.ncols
            print(os.getcwd(),"行数%d，列数%d"%(nrows,ncols))
            for i in range(1,nrows):
                row_data=sheet.row_values(i)
                print(row_data)
                case=Case()
                case.inter_name=row_data[1]
                case.case_name=row_data[2]
                case.method=row_data[3]
                case.url=row_data[4]
                case.data=row_data[5]
                case.header=row_data[6]
                case.msg=row_data[7]
                case.code=row_data[8]
                case.expect=row_data[9]
                case.actual=row_data[11]
                case.status=row_data[10]
                db.session.add(case)
                db.session.commit()     
    return redirect(url_for('yongli'))
@app.route('/daoru_in')
def daoru_in():
    return render_template('uploadinter.html')
@app.route('/daoru_inter',methods=['GET','POST'])
def daoru_inter():
    if request.method=='POST':
        file=request.files.get('file')
        f=file.read()
        book=xlrd.open_workbook(file_contents=f)
        sheetnames=book.sheet_names()
        for sheetname in sheetnames:
            sheet=book.sheet_by_name(sheetname)
            nrows=sheet.nrows
            ncols=sheet.ncols
            print(os.getcwd(),"行数%d，列数%d"%(nrows,ncols))
            for i in range(1,nrows):
                row_data=sheet.row_values(i)
                print(row_data)
                inter=Interface()
                inter.pro_name=row_data[0]
                inter.inter_name=row_data[1]
                inter.url=row_data[2]
                inter.method=row_data[3]
                inter.header=row_data[4]
                db.session.add(inter)
                db.session.commit()     
    return redirect(url_for('interface')) 
@app.route('/down_inter')
def down_inter():
    wb=xlwt.Workbook(encoding="utf-8")
    ws=wb.add_sheet("inter", cell_overwrite_ok=True)
    title=["项目名称","接口名称","接口地址","请求方法","接口header"]
    for i in range(0,len(title)):
        ws.write(0,i,title[i])
    row=1    
    inters=Interface.query.all()
    for inter in inters:
        ws.write(row,0,inter.pro_name)
        ws.write(row,1,inter.inter_name)
        ws.write(row,2,inter.url)
        ws.write(row,3,inter.method)
        ws.write(row,4,inter.header)
        row+=1    
    sio=BytesIO()
    wb.save(sio)
    sio.seek(0)
    response=make_response(sio.getvalue())
    response.headers['Content-type'] = 'application/vnd.ms-excel'  # 指定返回的类型
    response.headers['Content-Disposition'] = 'attachment;filename=inter.xls'  # 设定用户浏览器显示的保存文件名
    return response  
@app.route('/operate_case')
def operate_case():
    cases=Case.query.with_entities(Case.inter_name).distinct().all()#查询数据 并去重
    return render_template('operatecase.html',cases=cases)
@app.route('/operate_success',methods=['GET','POST'])
def operate_case_success():
    if request.method=='POST':
        selectdata=request.values.get("case")
        print(selectdata)
        cases=Case.query.filter(Case.inter_name == selectdata)
        print(cases)
        for case in cases:
            print(case)
            url=[]
            url.append(case.url)
            method=[]
            method.append(case.method)
            data=[]
            data.append(case.data)
            inter_name=[]
            inter_name.append(case.inter_name)
            case_name=[]
            case_name.append(case.case_name)
            header=[]
            header.append(case.header)
            msg=[]
            msg.append(case.msg)
            code=[]
            code.append(case.code)
            expect=[]
            expect.append(case.expect)
            status=[]
            status.append(case.status)
            actual=[]
            actual.append(case.actual)
            id=[]
            id.append(case.id)
            print(method,url,code,data)
            result=http_request.http_request(method[0], url[0], data[0])
            if result.json()["code"]==int(code[0]):
                print(result.json()["code"])
                status[0]=str(True)
                actual[0]=str(result.json())
            else:
                print(result.json()["code"])
                status[0]=str(False)
                actual[0]=str(result.json())
            addreport=Report(id=id[0],url=url[0],method=method[0],data=data[0],\
                             inter_name=inter_name[0],case_name=case_name[0],\
                             header=header[0],expect=expect[0],code=code[0],\
                             msg=msg[0],status=status[0],actual=actual[0])
            db.session.add(addreport)
            db.session.commit()      
    else:
        return render_template('operatecase.html')
    return redirect(url_for('report')) 
@app.route('/testreport')
def report():
    reports=Report.query.all()
    pass_count=Report.query.filter(Report.status==str(True)).count()
    fail_count=Report.query.filter(Report.status==str(False)).count()
    all_count=pass_count+fail_count
    count={
        "pass_count":pass_count,
        "fail_count":fail_count,
        "all_count":all_count,
        "reports":reports
        }
    return render_template('testreport.html',**count)
@app.route('/down_report')
def down_report():
    wb=xlwt.Workbook(encoding="utf-8")
    ws=wb.add_sheet("testreport", cell_overwrite_ok=True)
    title=["接口名称","用例名称","请求方法","接口url","请求参数","header","msg校验值","code校验值","预期结果","状态 ","实际结果"]
    for i in range(0,len(title)):
        ws.write(0,i,title[i])
    row=1    
    reports=Report.query.all()
    for case in reports:
        ws.write(row,0,case.inter_name)
        ws.write(row,1,case.case_name)
        ws.write(row,2,case.method)
        ws.write(row,3,case.url)
        ws.write(row,4,case.data)
        ws.write(row,5,case.header)
        ws.write(row,6,case.msg)
        ws.write(row,7,case.code)
        ws.write(row,8,case.expect)
        style=xlwt.XFStyle()
        font=xlwt.Font()
        font.colour_index=2
        style.font=font
        if case.status==str(True):
            ws.write(row,9,case.status)
        else:
            ws.write(row,9,case.status,style)
        ws.write(row,10,case.actual)
        row+=1    
    sio=BytesIO()
    wb.save(sio)
    sio.seek(0)
    response=make_response(sio.getvalue())
    response.headers['Content-type'] = 'application/vnd.ms-excel'  # 指定返回的类型
    response.headers['Content-Disposition'] = 'attachment;filename=testreport.xls'  # 设定用户浏览器显示的保存文件名
    return response
@app.route('/edit_report/<int:id>')
def edit_report(id):
    cases=Report.query.filter_by(id=id).all()
    return render_template('editreport.html',cases=cases)
@app.route('/edit_report_success/<int:id>',methods=['GET','POST'])
def edit_report_success(id):
    case=Report.query.filter_by(id=id).first()
    if request.method=='POST':
        case.case_name=request.form.get('casename')
        case.inter_name=request.form.get('intername')
        case.url=request.form.get('url')
        case.meth=request.form.get('meth')
        case.header=request.form.get('header')
        case.data=request.form.get('data')
        case.msg=request.form.get('msg')
        case.code=request.form.get('code')
        case.expect=request.form.get("expect")
        case.status=request.form.get('status')
        case.actual=request.form.get('actual')
        db.session.add(case)
        db.session.commit()
        return redirect(url_for('report'))  
@app.route('/delete_report/<int:id>')
def delete_report(id):
    report=Report.query.filter_by(id=id).first()
    db.session.delete(report)
    db.session.commit()
    return redirect(url_for('report')) 
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
   
if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)