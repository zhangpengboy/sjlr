from flask import Flask,request,session,render_template,Blueprint,flash, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
import pymysql
import hashlib
import datetime
pymysql.install_as_MySQLdb()


app=Flask(__name__)
app.config['SECRET_KEY'] = '123456'# flash密匙
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost:3306/app"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['DEBUG']=True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)

#创建Manager对象并指定要管理的app
manager=Manager(app)
# 创建Migrate对象，并指定关联的app和db
migrate=Migrate(app,db)
#为manager增加命令，允许做数据库的迁移操作
#为manager绑定一个db的子命令，该子命令执行操作由MigrateComand提供
manager.add_command('db',MigrateCommand)


# 注册蓝图
# app.register_blueprint(task_bp)

# 注册申请
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        # ------------
        # 账号  密码　昵称　性别　出生年月　email  电话　地址　头像　
        # ------------
        account=request.form.get("uaccount")
        password=request.form.get("password1")
        name=request.form.get("uname")
        sex=request.form.get("usex")
        age=request.form.get("uage")
        email=request.form.get("uemail")
        phone=request.form.get("uphone")
        try:
            f = request.files['file']
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
            # aa=datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')  # 时间节点
            bb=f.filename.split('.')[-1]
            imgurl = 'static/img/' + account + '.' +bb
            f.save(imgurl)
        except:
            imgurl = 'static/img/0.jpg'


        password=password.encode()
        pwd_temp=hashlib.sha1(password)
        password=pwd_temp.hexdigest()
        user = Users(account,password,name,sex,age,email,phone,imgurl)
        db.session.add(user)   #session 事物会话　记录对象任务
        db.session.commit()    #数据提交

        resp = make_response('')
        resp.set_cookie('account',account,-100) #cookie保持到浏览器关闭
        return render_template('login.html',params={account})

class Users(db.Model):
    __tablename__ = 'users'  #指明表名
    account= db.Column(db.String(20), primary_key=True)    #db.Column 真实存在的列
    password= db.Column(db.String(40),nullable=False)      #定义字段
    name= db.Column(db.String(20),nullable=False)
    sex=db.Column(db.String(5),nullable=False)
    age= db.Column(db.String(20))
    email= db.Column(db.String(40),nullable=False)
    phone= db.Column(db.String(20),nullable=False)
    imgurl=db.Column(db.String(50),nullable=False)

    def __init__(self,account,password,name,sex,age,email,phone,imgurl):
        self.account=account
        self.password=password
        self.name=name
        self.sex=sex
        self.age=age
        self.email=email
        self.phone=phone
        self.imgurl=imgurl

# 登录申请
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        url = request.headers.get('Referer','/')
        session['url'] = url
        if 'account' in session:
            return redirect(url)
        else:
            if 'account' in request.cookies:
                account = request.cookies['account']
                user = Users.query.filter_by(account=account).first()
                if user.account == account:
                    session['account']=account
                    return redirect(url)
                else:
                    resp = make_response(render_template('login.html',params={}))
                    resp.delete_cookie('account')
                    return resp
            else:
                return render_template('login.html',params={})
    else:
        uaccount = request.form.get("uaccount")
        upassword = request.form.get("upassword")
        upassword=upassword.encode()
        pwd_temp = hashlib.sha1(upassword)
        upassword = pwd_temp.hexdigest()
        print(uaccount,upassword)
        user=Users.query.filter_by(account=uaccount).first()
        print(user)
        try:
            if user.password==upassword:

                session['account']= uaccount
                try:
                    url = session['url']
                except:
                    url='/'
                resp = redirect(url)
                if 'isSaved' in request.form:
                    resp.set_cookie('account',uaccount,60*60*24*365)
                return resp
            else:
                err = '用户名或密码错误'
                return render_template('login.html',params=locals())
        except :
            err = '用户名不存在'
            return render_template('login.html',params=locals())


@app.route('/logout')
def logout():
    url = request.headers.get('Referer','/')
    resp = redirect(url)
    if 'account' in request.cookies:
        resp.delete_cookie('account')
    if 'account' in session:
        del session['account']
    return resp

# 任务路由视图
# @task_bp.route("/risetask",methods=["POST",'GET'])
@app.route("/risetask",methods=["POST",'GET'])
def rise_task():
    if request.method=="GET":
        return render_template("risetask.html")
    else:
        tip=request.form.get('tip') #任务类型
        uid = request.form.get('uid')#发布任务用户id
        pmtime = request.form.get('pmtime')#任务发布时间
        task_id = str(uid) + str(pmtime)  # 发布任务代码
        # 任务详情　赏金　时间ｘ３　地点
        title = request.form.get('title') #任务标题
        content = request.form.get('text')# 任务详情
        salary = request.form.get('salary')# 赏金
        smtime = request.form.get('smtime')# 任务最迟开始时间
        sptime = request.form.get('sptime')# 任务最迟结束时间
        position = request.form.get('position')# 任务地点
        try:
            f = request.files['file']
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
            aa=datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')  # 时间节点
            bb = f.filename.split('.')[-1]
            task_imgurl = 'static/img/' + uid +aa + '.' + bb
            f.save(task_imgurl)
        except:
            task_imgurl = 'static/img/0.jpg'

        # ------------（任务id，任务类型，任务标题，发布者id，任务详情，赏金，发布时间，接受截止时间，任务截止时间，任务地点）
        task = Tasks(task_id, tip, title, uid, content, salary, pmtime, smtime, sptime, position,task_imgurl)
        db.session.add(task)  # session 事物会话　记录对象任务
        db.session.commit()  # 数据提交
        if content and uid and pmtime and salary and smtime and sptime and position:
            flash("任务发布成功，任务单号%s,点击跳转" % task_id)
            return render_template('risetask.html')
        if not content and not uid and not pmtime and not salary and not smtime and not sptime and not position:
            return render_template('risetask.html')

#任务类
class Tasks(db.Model):
    __tablename__ = 'tasks'  #指明表名
    task_id= db.Column(db.String(20), primary_key=True)    #db.Column 真实存在的列
    tip = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    uid= db.Column(db.String(40),nullable=False)      #定义字段
    content= db.Column(db.String(400),nullable=False)
    salary=db.Column(db.String(5),nullable=False)
    pmtime= db.Column(db.String(20))
    smtime= db.Column(db.String(20),nullable=False)
    sptime= db.Column(db.String(20),nullable=False)
    position= db.Column(db.String(20),nullable=False)
    task_imgurl=db.Column(db.String(100),nullable=False)


    def __init__(self,task_id, tip, title, uid, content, salary, pmtime, smtime, sptime, position,task_imgurl):
        self.task_id=task_id
        self.tip = tip
        self.title=title
        self.uid=uid
        self.content=content
        self.salary=salary
        self.pmtime=pmtime
        self.smtime=smtime
        self.sptime=sptime
        self.position=position
        self.task_imgurl=task_imgurl

# 任务详情页跳转 task_id=20190112xxx
@app.route("/task")
def task_info():
    pass
    # return render_template("task//%s.html" % task_id)




# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # kw = request.args.get('kw')
    # if not kw:
    #     pass
    #     # result = db.session.query(Tasks).filter().all()
    # else:
    #     pass
    #     # result = db.session.query(Tasks).filter(Tasks.task_id=task_id).all()
    #     result = db.session.query(Tasks).filter(Tasks.title.like('%kw%')).all()
    #     result = db.session.query(Tasks).filter(Tasks.position.like('%kw%')).all()
    if 'account' in session:
        account = session['account']
    else:
        if 'account' in request.cookies:
            account = request.cookies['account']
        else:
            account = ''
    # if account:
    #     return render_template('index.html', result=result)
    # else:
    #     return render_template('index.html',result=result)
    return render_template('index.html',params=locals())

# db.create_all()  #创建所有所已定义的表

if __name__=="__main__":
    manager.run()
    # app.run()