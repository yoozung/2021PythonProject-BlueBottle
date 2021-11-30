from flask import request, render_template, redirect, Blueprint, session
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from models import BoardService, Merchandise

path = os.path.dirname(os.path.abspath(__file__))
print(path)

service = BoardService()

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/list')
def list():
    blist = service.getAll()
    return render_template('board/list.html', blist=blist)

@bp.route('/add')
def addForm():
    if session['flag'] == False:
        flag = False
    else:
        flag = True
    return render_template('board/form.html', flag=flag)


@bp.route('/add', methods=['POST'])
def add():
    writer = request.form['writer']
    engName = request.form['engName']
    krName = request.form['krName']
    price = request.form['price']
    imgLink = request.form['imgLink']
    service.addBoard(Merchandise(writer=writer, engName=engName, krName=krName, price=price, imgLink=imgLink))
    return redirect('/board/list')

@bp.route('/detail/<int:num>')
def detail(num):
    b = service.getBoard(num)
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
    return render_template('board/detail.html', b=b, flag=flag, msg=msg, paybutton=paybutton)

@bp.route('/edit', methods=['POST'])
def edit():
    num = request.form['num']
    engName = request.form['engName']
    krName = request.form['krName']
    price = request.form['price']
    service.editBoard(Merchandise(num=num, engName=engName, krName=krName, price=price))
    return redirect('/board/list')


@bp.route('/del/<int:num>')
def boardDel(num):
    service.delBoard(num)
    return redirect('/board/list')