from flask import request, render_template, redirect, Blueprint, session
from models import BeanService, Bean

service = BeanService()

bp = Blueprint('bean', __name__, url_prefix='/bean')

@bp.route('/list')
def list():
    beanlist = service.getAll()
    return render_template('bean/list.html', beanlist=beanlist)

@bp.route('/add')
def addForm():
    if session['flag'] == False:
        flag = False
    else:
        flag = True
    return render_template('bean/form.html', flag=flag)


@bp.route('/add', methods=['POST'])
def add():
    writer = request.form['writer']
    nameE = request.form['nameE']
    nameK = request.form['nameK']
    price = request.form['price']
    taste = request.form['taste']
    origin = request.form['origin']
    url = request.form['url']
    service.addBean(Bean(writer=writer, nameE=nameE, nameK=nameK, price=price, taste=taste, origin=origin, url=url))
    return redirect('/bean/list')

@bp.route('/detail/<int:num>')
def detail(num):
    b = service.getBean(num)
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
    return render_template('bean/detail.html', b=b, flag=flag, msg=msg, paybutton=paybutton)

@bp.route('/edit', methods=['POST'])
def edit():
    num = request.form['num']
    nameE = request.form['nameE']
    nameK = request.form['nameK']
    taste = request.form['taste']
    origin = request.form['origin']
    price = request.form['price']
    service.editBean(Bean(num=num, nameE=nameE, nameK=nameK, taste=taste, origin=origin, price=price))
    return redirect('/bean/list')

@bp.route('/out/<int:num>')
def delete(num):
    service.delBean(num)
    return redirect('/bean/list')