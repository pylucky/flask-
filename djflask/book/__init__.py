


from flask import Blueprint
##蓝图



app_book=Blueprint("app_book",__name__,template_folder="templates",static_folder="static")

#调用试图里面的方法
from book.views import lists,add,edit,delete


 
