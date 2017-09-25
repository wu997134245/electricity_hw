from flask import Blueprint,render_template,request,redirect,session
from DB import *
from redis_con import r
db = getDB()



user = Blueprint('user',__name__)



@user.route('/',methods = ['GET','POST'])
def user_login():
    second = request.values.get('second')
    if second == None:
        msg =''
        return render_template('login.html',msg = msg)
    name = request.values.get('cname')
    pwd = request.values.get('cpwd')
    sql = "select * from user where clogin = '%s' and cpwd ='%s'" % (name,pwd)
    ro,res = db.query(sql)
    if ro == 1:
        msg = ''
        session['name'] = request.form['cname']
        name = session['name']
        data = [{}, {}]
        r.set(name, data=data)
        return redirect('/product_list')
    else:
        msg = 'username or password error!'
        return render_template('login.html',msg = msg)




@user.route('/logout')
def user_logout():
    name = session['name']
    print  r.dele(name)
    return redirect('/')





# data = [{}, {}]
# r.set(session['name'], data=data)
