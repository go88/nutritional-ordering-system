# coding: utf-8

from app.route import app
from app.db import mysql_oper

from app.entity.entity_user import User
from app.entity.instance import INSTANCE

if __name__ == "__main__":

    # 实例化全局变量USER
    INSTANCE.USER = User()

    # 与数据库建立连接
    try:
        INSTANCE.CUR = mysql_oper.create_connect()
    except BaseException as err:
        print("except: " + str(err))

    # app.run()
    # 默认使用host接受全部ip访问
    # app.run(host="0.0.0.0")
    # debug使用
    app.run(debug=True)
