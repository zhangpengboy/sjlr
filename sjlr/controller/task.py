
'''任务视图函数'''
from . import task_bp
from flask import request,Blueprint,render_template,flash

from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()



@task_bp.route("/risetask",methods=["POST",'GET'])
def rise_task():
    # ------------
    uid = request.form.get('uid')#用户id
    pmtime = request.form.get('pmtime')#任务发布时间
    task_id =  str(uid) + str(pmtime) # 发布任务代码
    # 任务详情　赏金　时间ｘ３　地点
    content = request.form.get('text')# 任务详情
    salary = request.form.get('salary')# 赏金
    smtime = request.form.get('smtime')# 任务最迟开始时间
    sptime = request.form.get('sptime')# 任务最迟结束时间
    position = request.form.get('position')# 任务地点
    # ------------（讲道理，这里需要个新的数据库表，但是我不太会后端与数据库交互，先随便弄点）

    user = Users(account, password, name, sex, age, email, phone)
    db.session.add(user)  # session 事物会话　记录对象任务
    db.session.commit()  # 数据提交
    if content and uid and pmtime and salary and smtime and sptime and position:
        flash("任务发布成功，任务单号%s,点击跳转" % task_id)
        return render_template('risetask.html')
    if not content and not uid and not pmtime and not salary and not smtime and not sptime and not position:
        return render_template('risetask.html')

class Tasks(db.Model):
    __tablename__ = 'users'  #指明表名
    account= db.Column(db.String(20), primary_key=True)    #db.Column 真实存在的列
    password= db.Column(db.String(40),nullable=False)      #定义字段
    name= db.Column(db.String(20),nullable=False)
    sex=db.Column(db.String(5),nullable=False)
    age= db.Column(db.String(20))
    email= db.Column(db.String(20),nullable=False)
    phone= db.Column(db.Integer,nullable=False)

    def __init__(self,account,password,name,age,email,phone):
        self.account=account
        self.password=password
        self.name=name
        self.sex=sex
        self.age=age
        self.email=email
        self.phone=phone

db.create_all()  #创建所有所已定义的表