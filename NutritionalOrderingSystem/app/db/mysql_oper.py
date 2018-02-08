# coding: utf-8
'''
数据库操作类

建立连接 create_connect()

提供 增 删 改 查 函数
'''

import pymysql as mysql

from app.entity.entity_user import User
from app.entity.instance import INSTANCE



def create_connect():
    '''
    与MySQL数据库建立连接

    返回：pymysql.connect.cursor
    '''
    conn = mysql.connect(
    host="localhost",
    port=3309,
    user="root",
    passwd="123456",
    db="nutritional_ordering_system",
    )
    return conn.cursor()


def find_user(username):
    '''
    查询表中的数据

    返回一个User类
    '''
    sql = "select * from tb_user where username = '" + username + "'"
    INSTANCE.CUR.execute(sql)
    user = User()
    user.username, user.nickname, user.password, \
    user.address, user.phoneNumber, user.gender, \
    user.age, user.height, user.weight, user.waist, \
    user.BFR, user.BMR = INSTANCE.CUR.fetchone()
    return user


def insert_user(username, passwd):
    '''
    添加一条数据

    必须要username和password
    '''
    sql = "insert into tb_user values('" + username + "','" + username + \
        "','" + passwd + "',null,null,null,null,null,null,null,null,null)"
    print(sql)
    INSTANCE.CUR.execute(sql)
    # find_data()
    print("添加成功")


def alter_user(username, attribution, value):
    '''
    修改某个账户的某一属性

    修改账户user的attr属性为value
    '''
    sql = "update tb_user set " + attribution + " = " + \
        value + " where username = " + username + ""
    print(sql)
    INSTANCE.CUR.execute(sql)
    # find_data()
    print("修改成功")


def delete_user(username):
    '''
    删除某条数据通过关键字username
    '''
    sql = "delete from tb_user where username = {}".format(username)
    INSTANCE.CUR.execute(sql)
    # find_data()
    print("删除成功")
