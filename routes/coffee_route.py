from flask import request, render_template, redirect, Blueprint, session
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models import CoffeeService, Coffee
from models import MemService, Member
import json

service = CoffeeService()
service2 = MemService()

bp = Blueprint('coffee', __name__, url_prefix='/coffee')

# 조회(R) : 커피 리스트
@bp.route('/list')
def list():
    blist = service.getAll()
    return render_template('coffee/list.html', blist=blist)

# 생성(C) 페이지 이동, GET방식 
@bp.route('/add')
def addForm():
    if session['flag'] == False:
        flag = False
    else:
        flag = True
    return render_template('coffee/form.html', flag=flag)


# 생성(C) : 커피 제품 등록, POST방식
@bp.route('/add', methods=['POST'])
def add():
    writer = request.form['writer']
    name2 = request.form['name2']
    name = request.form['name']
    price = request.form['price']
    img = request.form['img']
    service.addCoffee(Coffee(writer=writer, name=name, name2=name2, price=price, img=img))
    return redirect('/coffee/list')

# 상세 페이지 이동 -> list.html -> detail.html
@bp.route('/detail/<int:num>') #<a href="/board/detail/{{b.num}}">
def detail(num):
   b = service.getCoffee(num)
   if session['flag'] == False:
       flag = False
       paybutton = True
       msg = 'readonly'
   else:
       if b.writer == session['login_id']:
           flag = True
           paybutton = False
           msg = ''
       else:
           flag = False
           paybutton = True
           msg = 'readonly'
   return render_template('coffee/detail.html', b=b, flag=flag, msg=msg, paybutton=paybutton)

@bp.route('/edit', methods=['POST'])
def edit():
    num = request.form['num']
    name2 = request.form['name2']
    name = request.form['name']
    price = request.form['price']
    service.editCoffee(Coffee(num=num, name=name, name2=name2, price=price))

    return redirect('/coffee/list')

@bp.route('/del/<string:num>')
def delete(num):
    service.delCoffee(num)
    return redirect('/coffee/list')