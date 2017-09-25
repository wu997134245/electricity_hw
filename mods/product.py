from flask import Blueprint,render_template,request,session
from DB import *
from redis_con import r
import json
db = getDB()


product = Blueprint('product',__name__)


@product.route('/product_list')
def product_list():
    row,res = db.query('select * from product')
    return render_template('product_list.html',res = res)


@product.route('/product_dis/<id>')
def product_dis(id):
    row,res = db.query('select * from product where id = "%s"' % id)
    res = res[0]
    return render_template('product_dis.html',res = res)


@product.route('/user_data')
def user_data():
    query_column = ['id','cname','cprice']
    query_column_str=','.join(query_column)
    print query_column_str




    row,res = db.query('select %s from product' %(query_column_str))
    data = [{'name':'tom','age':18},{'name':'alice','age':28},{'name':'bob','age':8},{'name':'hey','age':108}]
    res.append(query_column)




    print '%s' % res
    return json.dumps(res)
