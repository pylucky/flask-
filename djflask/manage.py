
from flask import Flask,request,url_for,redirect,render_template,jsonify,current_app

from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate,MigrateCommand
import json
import redis
import datetime

##session 保存到redis

from flask_session import Session


### CSRF保护
from flask_wtf.csrf import CsrfProtect
 

app=Flask(__name__)


##数据库配置

class Config():

    SQLALCHEMY_DATABASE_URI="mysql://root:123456@127.0.0.1:3306/djflask"
    ##跟踪设置
    SQLALCHEMY_TRACK_MODIFTCATIONS=True
    ##显示原始SQL语句
    # app.config['SQLALCHEMY_ECHO']=True
    DEBUG=True

    SECRET_KEY="DSAFDSAFSFF"

    ##flask_session

    SESSION_TYPE="redis"
    SESSION_REDIS=redis.StrictRedis(host="127.0.0.1",port=6379)
    SESSION_USER_SIGNER=True  ## 对cooike中的session_id 隐藏
    PERMANENT_SESSION_LIFETIME=3600*24  ##session 过期时间


app.config.from_object(Config)

##配置redis

redis_store=redis.StrictRedis(host="127.0.0.1",port=6379)



db=SQLAlchemy(app)
#变成 manage


####数据库

###作者表
class Author(db.Model):
  
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),unique=False)

    ##
    books=db.relationship('Book',backref="author")



##图书表
class Book(db.Model):

    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)

    #
    create_time=db.Column(db.DateTime,default=datetime.datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('author.id'))



migrate=Migrate(app,db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)

Session(app)
CsrfProtect(app)





@app.route('/')

def  index():
   
    ##查询作者信息
    author=Author.query.all()
    book=Book.query.all()
        
    return  render_template("index.html")





from book import app_book
##注册蓝图应用
### 127.0.0.1:8000/
app.register_blueprint(app_book,url_prefix="/book")


if __name__=="__main__":

    db.create_all()
   

    manager.run()