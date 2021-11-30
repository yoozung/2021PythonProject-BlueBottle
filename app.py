from flask import Flask, request, render_template, redirect, session
from models import db, migrate, BoardService
import routes.coffee_route as cr
import routes.mem_route as mr
import routes.board_route as br
import routes.bean_route as bean
import config

service = BoardService()

#플라스크 객체 생성
app = Flask(__name__)

#시크릿 키 생성
app.secret_key = 'asfaf'

#플라스크 컨피그에 사용자정의 컨피그 추가
app.config.from_object(config)

#블루 프린트 등록
app.register_blueprint(mr.bp)
app.register_blueprint(br.bp)
app.register_blueprint(bean.bp)
app.register_blueprint(cr.bp)

# ORM 연동
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def root():
    blist = service.getAll()
    if 'flag' not in session.keys():
        session['flag']=False
    return render_template('main.html', blist=blist)


if __name__ == '__main__':
    app.run()#flask 서버 실행