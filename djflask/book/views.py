

from book import app_book
from flask import Flask,request,url_for,redirect,render_template,jsonify,current_app
from manage import  Author,Book
from flask_sqlalchemy import SQLAlchemy

###图书首页




from manage import db

###图书列表页
@app_book.route('/list')

def  lists():
    
    ##查询作者信息
    author=Author.query.all()
    book=Book.query.all()
        
    for  i in book:
        print(i.create_time )
    return  render_template("list.html",author=author)

#### 图书添加
@app_book.route("/add",methods=["POST","GET"])
def  add():
    
    if request.method=="GET":
        

      
        return render_template("add.html")
        

    if request.method=="POST":

        au_name=request.form.get("authorname")
        
        bk_name=request.form.get("bookname")

      
        ##判断数据完整性

        if not all([au_name,bk_name]):
            error1={"error1":"<h1 style='color:red'>数据没有填完整</h1>"}
            return render_template("add.html",**error1)

        ###如果作者存在,添加作者和书籍 

        author=Author.query.filter_by(name=au_name).first()
  
        if author:
            ###增加书

              ##检测图书重复
            book_name=Book.query.filter_by(name=bk_name).first()
            if book_name:
                error2={"error2":"<h1 style='color:red'>图书已存在</h1>"}
                return render_template("add.html",**error2)

          
            book=Book(name=bk_name,author_id=author.id)

            #  ## 把新作者添加进去
            db.session.add(book)
           
            db.session.commit()

            return redirect(url_for("app_book.lists"))

        else:

            ##作者不存在 
            ###加 书和作者
            new_author = Author(name=au_name)
            db.session.add(new_author)
            db.session.commit()

            new_book = Book(name=bk_name, author_id=new_author.id)
            db.session.add(new_book)
            db.session.commit()

            return redirect(url_for('app_book.lists'))
  


##图书删除  作者删除
@app_book.route('/del/<bookid>') 
def delete(bookid): 

    ##更具ID删除对应的书
    ## bookid
    book=Book.query.get(bookid)


    # ### 更具 author_id 删除作者的 id 
    # # uid=Author.query.get(aid)
    # uid=book.author_id
  
    # author=Author.query.filter_by(id=uid).first()

    # db.session.delete(author)

    db.session.delete(book)

    db.session.commit()
    
    return  redirect(url_for('app_book.lists'))





##图书编辑
@app_book.route('/edit/<forid>',methods=["GET","POST"])
def  edit(forid):
    ##由 书id  查询作者
    ## 一本书 对应一个作者    |||||NO( 一个作者 所有书 )
    if request.method=="GET":
       

        book=Book.query.filter_by(id=forid)

            

        return  render_template("edit.html",book=book)


    if request.method=="POST":
        
        ##调用CSRF


        authorname=request.form.get("authorname")
        bookname=request.form.get("bookname")
        # print(authorname)
        print(bookname)
        ##数据检测
        if not all([authorname,bookname]):

            error1={"error1":"<h1 style='color:red'>数据不完整</h1>"}

            return  render_template("edit.html",**error1)

        ##更新作者

        ## post 需要作者ID,图书ID 隐藏域传过来 aid,bid 
       

        ##作者id
        aid=request.form.get("aid")
        author=Author.query.filter_by(id=aid).update({"name":authorname})
        

        ##更新图书id 
        bid=request.form.get("bid")
        
        book=Book.query.filter_by(id=bid).update({"name":bookname})
        ##反查询
        db.session.commit()

        return  redirect(url_for('app_book.lists'))