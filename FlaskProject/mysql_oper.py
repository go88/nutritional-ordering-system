# coding: utf-8
import pymysql as mysql
from user import User

# 建立连接
conn = mysql.connect(
    host="localhost",
    port=3309,
    user="root",
    passwd="123456",
    db="test_flask",
)
user = User()
cur = conn.cursor()


# 查询表中的数据并打印
def find_data(username):
    # try:
    sql = "select * from tb_user where username = '" + username + "'"
    cur.execute(sql)
    user.username, user.nickname, user.password, user.address, user.phoneNumber, user.gender, user.age, user.height, user.weight, user.waist, user.BFR, user.BMR = cur.fetchone(
        )
    return user


# 添加一条数据
def insert_data(username, passwd):
    sql = "insert into tb_user values('" + username + "','" + username + "','" + passwd + "',null,null,null,null,null,null,null,null,null)"
    print(sql)
    cur.execute(sql)
    # find_data()
    print("添加成功")


# 修改某条数据
def alter_data(username, attribution, value):
    sql = "update tb_user set " + attribution + " = " + value + " where username = " + username + ""
    print(sql)
    cur.execute(sql)
    # find_data()
    print("修改成功")


# 删除某条数据
def delete_data(username):
    sql = "delete from tb_user where username = %s"(username)
    cur.execute(sql)
    # find_data()
    print("删除成功")

# cur.close()
# conn.close()
