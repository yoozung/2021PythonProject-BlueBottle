from flask import request, render_template, redirect, Blueprint, session
from models import MemService, Member
from models import BoardService, Merchandise
service = MemService()
service2 = BoardService()
bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/join')
def joinForm():
    return render_template('member/form.html')

@bp.route('/join', methods=['POST'])
def join():
    id = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    email = request.form['email']
    service.join(Member(id=id, pwd=pwd, name=name, email=email))
    return render_template('member/login.html')

@bp.route('/login')
def loginForm():
    return render_template('member/login.html')

@bp.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    flag = service.login(id, pwd)
    blist = service2.getAll()
    return render_template('main.html', blist=blist)

@bp.route('/myinfo')
def myinfo():
    m = service.myInfo()
    return render_template('member/detail.html', m=m)

@bp.route('/out')
def delete():
    service.out()
    blist = service2.getAll()
    return render_template('main.html', blist=blist)

@bp.route('/logout')
def logout():
    service.logout()
    blist = service2.getAll()
    return render_template('main.html', blist=blist)

@bp.route('/edit', methods=['POST'])
def edit():
    pwd = request.form['pwd']
    # name = request.form['name']
    # email = request.form['email']
    service.editMyInfo(pwd=pwd)
    blist = service2.getAll()
    return render_template('main.html', blist=blist)
