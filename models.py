from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import session

db = SQLAlchemy()
migrate = Migrate()

class Member(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    pwd = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

class Bean(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.String(20), nullable=True)
    nameE = db.Column(db.String(20), nullable=False)
    nameK = db.Column(db.String(20), nullable=False)
    taste = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)

class Merchandise(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.String(20), nullable=False)
    engName = db.Column(db.String(50), nullable=False)
    krName = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    imgLink = db.Column(db.String(200), nullable=True)

class Coffee(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(20), nullable=True)
    name2 = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    img = db.Column(db.String(255), nullable=True)

class MemService:
    def join(self, m: Member):  # 회원가입
        db.session.add(m)
        db.session.commit()

    def login(self, id: str, pwd: str):  # 로그인
        mem = Member.query.get(id)
        if mem is not None:
            if pwd == mem.pwd:
                session['login_id'] = id
                session['flag'] = True
                return True
        return False

    def myInfo(self):  # 로그인 한 id로 검색한 객체 반환
        id = session['login_id']
        return Member.query.get(id)

    def editMyInfo(self, pwd: str):  # 새 pwd받아서 현재 로그인 중인 id로 검색하여 수정
        mem = self.myInfo()
        mem.pwd = pwd
        # mem.name = name
        # mem.email = email
        db.session.commit()

    def logout(self):  # session에서 id 삭제 및 flag =False로 변환
        session.pop('login_id')
        session['flag'] = False

    def out(self):  # 로그인한 id를 db에서 삭제. 로그아웃 처리.
        mem = self.myInfo()
        db.session.delete(mem)
        db.session.commit()
        self.logout()



class BeanService:
    # 원두등록
    def addBean(self, b:Bean):
        db.session.add(b)
        db.session.commit()

    def getBean(self, num):
        return Bean.query.get(num)

    def getAll(self):
        return Bean.query.order_by(Bean.num.desc())

    def getByName(self, name):
        return Bean.query.filter(Bean.name.like('%'+name+'%')).all()

    def editBean(self, b:Bean):
        bean = self.getBean(b.num)
        bean.nameE = b.nameE
        bean.nameK = b.nameK
        bean.price = b.price
        db.session.commit()

    def delBean(self, num:int):
        bean = self.getBean(num)
        db.session.delete(bean)
        db.session.commit()

class BoardService:
    def addBoard(self, b:Merchandise):#작성자id, title, content
        # b.w_date = datetime.now()
        db.session.add(b)
        db.session.commit()

    def getBoard(self, num):
        return Merchandise.query.get(num)

    def getAll(self):
        db.session.commit()
        return Merchandise.query.order_by(Merchandise.num.asc())

    def getByTitle(self, tit):
        return Board.query.filter(Board.title.like('%'+tit+'%')).all()

    def getByWriter(self, writer):
        mem = Member.query.get(writer)
        if mem is not None:
            return mem.board_set #작성자가 쓴 모든 글 검색해서 반환

    def editBoard(self, b:Merchandise):
        b2 = self.getBoard(b.num)
        b2.engName = b.engName
        b2.krName = b.krName
        b2.price = b.price
        #b2.w_date = datetime.now()
        db.session.commit()

    def delBoard(self, num):
        b = self.getBoard(num)
        db.session.delete(b)
        db.session.commit()

class CoffeeService:

    def __init__(self):
        self.cnt = 12

    def addCoffee(self, c:Coffee):
        self.cnt += 1
        c.num = self.cnt
        c.img = ''
        # db.session은 db와 연결하는 세션임. 접속된 상태를 의미. db를 처리하기 위해서는 이 세션이 필요하다.
        db.session.add(c)
        db.session.commit() #커밋 , c,u,d는 꼭 커밋을 해준다.

    def getCoffee(self, num:int):
        return Coffee.query.get(num)

    def getAll(self):
        db.session.commit()
        return Coffee.query.order_by(Coffee.num.asc())

    def editCoffee(self, c:Coffee):
        coffee = self.getCoffee(c.num) #c객체의 num에 해당하는 객체 조회
        coffee.name = c.name #이름 수정
        coffee.price = c.price #가격 수정
        db.session.commit() #커밋

    def delCoffee(self, num:int):
        coffee = self.getCoffee(num)
        db.session.delete(coffee)
        db.session.commit()

