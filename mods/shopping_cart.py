# coding=utf-8
from flask import Blueprint,render_template,request,redirect, session
from DB import *
import redis
import pickle
import copy
from redis_con import r
db = getDB()

cart = Blueprint('cart', __name__)


class Redis():
    def __init__(self, host,port, password):
        pool = redis.ConnectionPool(host=host, port=port, password=password)
        self.r = redis.Redis(connection_pool=pool)


    def set(self,name,data):
        data = pickle.dumps(data)
        self.r.set(name,data,)


    def get(self,name):
        data = self.r.get(name)
        if not data:
            return {}
        return pickle.loads(data)

    def dele(self,name):
        status = self.r.delete(name)
        return status

    def hmset(self,name,data):
        data = pickle.dumps(data)
        self.r.hmset(name,data)

    def hmget(self,name):
        data = pickle.loads(self.r.hgetall(name))
        return data





@cart.route('/cart')
def cart_page():
    name = session['name']
    cart_list = r.get(name)
    print cart_list
    if not cart_list[0]:
        return render_template('cart_list_null.html')
    data = copy.deepcopy(cart_list[0])

    print data ,'s'
    key_list = data.keys()

    row, res = db.query('select * from product where id in %s' % ('(' + str(key_list).strip('[]') + ')'))
    print res
    pirce_dict = {int(i[0]): float(i[4]) for i in res}

    for i in pirce_dict:
        data.get(i).append(pirce_dict[i])

    for i in data:
        total_pirce = data[i][0] * data[i][1]
        data[i].append(total_pirce)

    print data

    cart_list[1] = data
    all_pirce = 0
    for i in data:
        all_pirce = all_pirce + data[i][2]

    data['product_data'] = res
    print cart_list ,'chuliwancheng'
    r.set(name,cart_list)


    return render_template('cart_list.html',res=res, cart_dict = data,all_pirce= all_pirce)



@cart.route('/cart/add')
def product_add_to_cart():
    global value

    pid = int(request.values.get("pid"))
    pcount = int(request.values.get("pcount"))
    name = session['name']
    cart_list = r.get(name)
    print cart_list, 'start'
    data = cart_list[0]
    if data:
        old_pcount = data.get(pid)
        if old_pcount:
            pcount = old_pcount[0] + pcount
            data[pid][0] = pcount
        else:
            key = pid
            value = [pcount]
            data[key] = value
        print data
    else:
        key = pid
        value = [pcount]
        data = {}
        data[key] = value
    print data, 'gouwu'
    cart_list[0] = data
    r.set(name,cart_list)
    print cart_list, 'list'
    return 'ID %s  have %s 个' % (int(pid) , data[pid][0])


@cart.route('/cart/remove')
def product_remove():
    name = session['name']
    pid = int(request.values.get("pid"))
    data = r.get(name)
    del data[0][pid]
    del data[1][pid]
    r.set(name,data)
    return '1'


@cart.route('/cart/account')
def product_accout():
    name = session['name']
    data = r.get(name)
    print data
    res =  data[1]['product_data']
    return render_template('order.html',res = res)



